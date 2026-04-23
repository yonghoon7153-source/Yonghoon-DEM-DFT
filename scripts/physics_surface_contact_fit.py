#!/usr/bin/env python3
"""Physics mode surface-contact scaling law — complete form overhaul.

Physical insight (Yonghoon): DEM is a point-contact model (Hertzian
elastic overlap); we elevated it to surface-contact via Tabor plastic
+ hemisphere caps. Surface-contact resistance is **tube/film-like
(R ∝ L/(σ·A))**, not constriction-like (R ∝ 1/√A). So the Physics-
mode scaling law should use **per-contact area directly**, not
coverage (a fraction that was a constriction proxy in Hertzian).

Proposed form (Physics-native):
    σ_phys = σ_grain · (φ - φc)^α · CN^β · A_hop^γ · f_p^δ · τ^μ

A_hop = path_hop_area_mean_physics (μm², averaged along percolation
        paths) — directly reflects surface-contact area scaling.

Expected:
  • γ near 1.0 (linear in A for bulk tube resistance)
  • α closer to 3D percolation theory (~2)
  • Simpler form, fewer overfit-prone blend/residual terms

Also tests alternative forms:
  • Form A: σ = σ_grain·(φ-φc)^α·CN^β·A_hop^γ·f_p^δ·τ^μ
  • Form B: σ = σ_grain·(φ-φc)^α·A_hop^γ·f_p^δ/τ^μ    (drop CN)
  • Form C: σ = σ_grain·φ^α·g_path^γ·f_p^δ/τ^μ          (use path_conductance directly)
  • Form D: σ = σ_grain·φ^α·A_bottleneck^γ·f_p^δ/τ^μ    (use bottleneck, series-limit)

Multi-start Nelder-Mead, R² + LOOCV per form.
"""
from __future__ import annotations
import sys, json
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.optimize import minimize

SCRIPTS = Path(__file__).parent
sys.path.insert(0, str(SCRIPTS))
from v32_exhaustive_refit import load_cases  # noqa: E402

SIGMA_GRAIN = 3.0


def load_phys_rows(cases):
    rows = []
    for c in cases:
        cid = c['case_id']; fm = None
        for base in ('results', 'archive'):
            for p in Path(f'webapp/{base}').rglob(f'{cid}/full_metrics.json'):
                try: fm = json.load(open(p))
                except Exception: pass
                break
            if fm is not None: break
        if fm is None: continue
        # Must have Physics path metrics + sigma_phys
        hop_p = fm.get('path_hop_area_mean_physics')
        bot_p = fm.get('path_hop_area_min_mean_physics')
        gc_p  = fm.get('path_conductance_mean_physics')
        sig_p = fm.get('sigma_full_mScm_physics')
        if not (hop_p and hop_p > 0): continue
        if not (sig_p and sig_p > 0): continue
        r = dict(c)
        r.update(hop_phys=float(hop_p),
                 bottleneck_phys=float(bot_p) if bot_p and bot_p>0 else 1e-6,
                 g_path_phys=float(gc_p) if gc_p and gc_p>0 else 1e-6,
                 sigma_phys=float(sig_p))
        rows.append(r)
    return rows


def fit_form(df, features_fn, param_names, x0_list, label, with_loocv=True):
    """Generic fit harness.
    features_fn(row) → dict of named log-features (already log-transformed).
    Model: log σ = b0 + Σ_k p_k · log_features[k]
    """
    n = len(df)
    # Build feature matrix (n × n_params)
    log_sig = np.log(df['sigma_phys'].values)
    feat_lists = [features_fn(df.iloc[i]) for i in range(n)]
    feat_names = param_names  # without b0
    X = np.zeros((n, len(feat_names)))
    for i, feats in enumerate(feat_lists):
        for j, fn in enumerate(feat_names):
            X[i, j] = feats[fn]
    sst = np.sum((log_sig - log_sig.mean())**2)

    def neg_r2(x):
        # x = [b0, p1, p2, ...]
        b0 = x[0]; ps = x[1:]
        lg = b0 + X @ ps
        if not np.all(np.isfinite(lg)): return 1e6
        return np.sum((log_sig - lg)**2) / sst

    best = None
    for x0 in x0_list:
        try:
            res = minimize(neg_r2, x0=x0, method='Nelder-Mead',
                           options={'xatol':1e-5,'fatol':1e-7,'maxiter':10000,'adaptive':True})
            if best is None or res.fun < best.fun: best = res
        except Exception: pass
    if best is None:
        return None
    x_best = best.x
    b0 = x_best[0]; ps = x_best[1:]
    lg = b0 + X @ ps
    r2 = 1 - np.sum((log_sig - lg)**2) / sst

    loocv = None
    if with_loocv:
        sse_loo = 0.0
        for i in range(n):
            mk = np.ones(n, bool); mk[i] = False
            Xm, ym = X[mk], log_sig[mk]
            sst_m = np.sum((ym - ym.mean())**2)
            def nr2_m(x):
                lg_ = x[0] + Xm @ x[1:]
                if not np.all(np.isfinite(lg_)): return 1e6
                return np.sum((ym - lg_)**2) / sst_m
            res_i = minimize(nr2_m, x0=x_best, method='Nelder-Mead',
                             options={'xatol':1e-4,'fatol':1e-6,'maxiter':3000,'adaptive':True})
            lg_i = res_i.x[0] + X[i] @ res_i.x[1:]
            sse_loo += (log_sig[i] - lg_i)**2
        loocv = 1 - sse_loo / sst
    s_pred = np.exp(lg)
    w20 = int(np.sum(np.abs(s_pred - df['sigma_phys'].values)/df['sigma_phys'].values < 0.20))

    print(f'\n── {label} ──')
    print(f'  R²     = {r2:.4f}')
    if loocv is not None:
        print(f'  LOOCV  = {loocv:.4f}')
    print(f'  w20    = {w20}/{n}')
    print(f'  b0 (ln σ_grain_eff) = {b0:+.3f}  → {np.exp(b0):.3f} mS/cm')
    for name, val in zip(feat_names, ps):
        print(f'  {name:20s} = {val:+.3f}')
    return dict(label=label, r2=float(r2),
                loocv=float(loocv) if loocv is not None else None,
                w20=int(w20), n=int(n), b0=float(b0),
                exponents={k: float(v) for k,v in zip(feat_names, ps)})


def main():
    rows = load_cases()
    data = load_phys_rows(rows)
    df = pd.DataFrame(data)
    if len(df) == 0:
        print('No Physics data. Run coverage_physics_vs_hertzian --all first.')
        return
    print(f'Loaded {len(df)} Physics cases with path-physics metrics.')

    # Sanity distributions
    print('\n=== input metric ranges ===')
    for col in ['phi', 'cn', 'tau', 'f_perc', 'hop_phys',
                'bottleneck_phys', 'g_path_phys', 'sigma_phys']:
        v = df[col].values
        print(f'  {col:18s}  [{v.min():.4g}, {v.max():.4g}]  median={np.median(v):.4g}')

    # ── FORM A: surface-contact full (α φ-φc, β CN, γ A_hop, δ f_p, μ τ)
    def feats_A(r):
        return dict(
            a_phi   = np.log(max(r['phi'] - 0.20, 1e-5)),  # α·log(φ-0.20)
            a_cn    = np.log(max(r['cn'], 1e-6)),
            a_hop   = np.log(max(r['hop_phys'], 1e-9)),
            a_fp    = np.log(max(r['f_perc'], 1e-3)),
            a_tau   = np.log(max(r['tau'], 1e-6)),
        )
    result_A = fit_form(df, feats_A,
        ['a_phi','a_cn','a_hop','a_fp','a_tau'],
        x0_list=[[1.0, 0.5, 1.5, 0.5, 3.0, -1.0],
                 [0.0, 2.0, 1.0, 1.0, 2.0, -2.0],
                 [0.5, 1.0, 0.8, 0.5, 4.0, -0.5]],
        label='FORM A: (φ-φc)^α · CN^β · A_hop^γ · f_p^δ · τ^μ')

    # ── FORM B: drop CN (redundant with A_hop?)
    def feats_B(r):
        return dict(
            a_phi = np.log(max(r['phi'] - 0.20, 1e-5)),
            a_hop = np.log(max(r['hop_phys'], 1e-9)),
            a_fp  = np.log(max(r['f_perc'], 1e-3)),
            a_tau = np.log(max(r['tau'], 1e-6)),
        )
    result_B = fit_form(df, feats_B,
        ['a_phi','a_hop','a_fp','a_tau'],
        x0_list=[[1.0, 0.5, 1.0, 3.0, -1.0],
                 [0.0, 2.0, 1.0, 2.0, -2.0]],
        label='FORM B: (φ-φc)^α · A_hop^γ · f_p^δ · τ^μ  (no CN)')

    # ── FORM C: path_conductance directly
    def feats_C(r):
        return dict(
            a_phi    = np.log(max(r['phi'] - 0.20, 1e-5)),
            a_gpath  = np.log(max(r['g_path_phys'], 1e-12)),
            a_fp     = np.log(max(r['f_perc'], 1e-3)),
            a_tau    = np.log(max(r['tau'], 1e-6)),
        )
    result_C = fit_form(df, feats_C,
        ['a_phi','a_gpath','a_fp','a_tau'],
        x0_list=[[1.0, 0.5, 1.0, 3.0, -1.0],
                 [0.0, 2.0, 0.5, 2.0, -1.0]],
        label='FORM C: (φ-φc)^α · g_path^γ · f_p^δ · τ^μ')

    # ── FORM D: bottleneck (series-limit physics)
    def feats_D(r):
        return dict(
            a_phi  = np.log(max(r['phi'] - 0.20, 1e-5)),
            a_bot  = np.log(max(r['bottleneck_phys'], 1e-9)),
            a_fp   = np.log(max(r['f_perc'], 1e-3)),
            a_tau  = np.log(max(r['tau'], 1e-6)),
        )
    result_D = fit_form(df, feats_D,
        ['a_phi','a_bot','a_fp','a_tau'],
        x0_list=[[1.0, 0.5, 0.5, 3.0, -1.0],
                 [0.0, 2.0, 0.3, 2.0, -1.0]],
        label='FORM D: (φ-φc)^α · A_bottleneck^γ · f_p^δ · τ^μ')

    # Comparison
    print('\n' + '=' * 75)
    print('=== FORM COMPARISON ===')
    print(f'{"form":55s}  {"R²":>7s}  {"LOOCV":>7s}  {"w20":>6s}')
    for r in [result_A, result_B, result_C, result_D]:
        if r is None: continue
        print(f'{r["label"][:55]:55s}  {r["r2"]:7.4f}  '
              f'{(r["loocv"] if r["loocv"] else float("nan")):7.4f}  '
              f'{r["w20"]:>3d}/{r["n"]}')

    # Save
    out_dir = Path('docs/figures/physics_regime')
    out_dir.mkdir(parents=True, exist_ok=True)
    with open(out_dir / 'physics_surface_contact_fit.json', 'w') as f:
        json.dump({'formA': result_A, 'formB': result_B,
                   'formC': result_C, 'formD': result_D}, f, indent=2)
    print(f'\n→ {out_dir}/physics_surface_contact_fit.json')


if __name__ == '__main__':
    main()
