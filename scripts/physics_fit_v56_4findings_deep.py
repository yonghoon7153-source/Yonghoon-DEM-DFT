#!/usr/bin/env python3
"""Physics-mode fit v56 — comprehensive deep-dive on all 4 findings.

Four explorations after v55 confirmed:
  Finding 1: σ_P = C · σ_H^0.83 (LOOCV 0.96)
  Finding 2: plastic penalty σ_P/σ_bulk_H ranges 0.09-0.36
  Finding 3: 8/13 features mode-invariant
  Finding 4: Lasso form > v29 (+0.06 LOOCV)
  Finding 5: σ_constr_H broken (no data)

This script digs deeper:

  PART 1 — σ_constr_only metric integrity check
      Discover the actual key name used in full_metrics.json. Report
      what sigma/constr-related keys exist. Recompute if needed.

  PART 2 — Lasso form distillation (Finding 4 deep)
      Take v55's 11 surviving features, fit them with proper bounded
      regression. Write out explicit equation. Compute effective
      exponent of (φ-φc) per CN, of τ per L. Per-term physical
      interpretation.

  PART 3 — Plastic penalty per-batch (Finding 2 deep)
      Stratify σ_P/σ_bulk_H ratio by batch (1mAh / 6mAh / 8mAh /
      particulate). For each batch: median, range, top driver from
      structural Lasso. Verify that (φ-φc)·CN dominates within each
      batch.

  PART 4 — 0.83 universality test (Finding 1 deep)
      Test σ_P = C·σ_H^γ across:
        - Whole dataset
        - Each batch (1mAh, 8mAh, 6mAh, particulate)
        - Different P:S subsets (5:5, 7:3, 0:10, 10:0)
      Is γ universal at 0.83? Or batch-dependent?
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


def part1_sigma_constr_diagnostic():
    """Find what sigma/constr keys exist; report stats per key."""
    print('\n' + '=' * 80, flush=True)
    print('PART 1 — sigma/constr metric integrity diagnostic', flush=True)
    print('=' * 80, flush=True)
    paths = (list(Path('webapp/results').rglob('full_metrics.json')) +
             list(Path('webapp/archive').rglob('full_metrics.json')))
    if not paths:
        print('  no metrics files found.', flush=True)
        return {}
    sample = json.load(open(paths[0]))
    sigma_keys = sorted([k for k in sample.keys()
                         if 'sigma' in k.lower() or 'constr' in k.lower()])
    print(f'  Found {len(sigma_keys)} sigma/constr-related keys in sample:',
          flush=True)
    for k in sigma_keys:
        print(f'    {k}', flush=True)

    # Population stats per key
    stats = {}
    print(f'\n  Population stats across {len(paths)} cases:', flush=True)
    print(f'  {"key":40s}  {"n":>4s}  {"min":>8s}  {"max":>8s}  '
          f'{"std":>8s}  {"unique":>6s}', flush=True)
    for k in sigma_keys:
        vals = []
        for p in paths:
            try:
                m = json.load(open(p))
                v = m.get(k)
                if v is not None and isinstance(v, (int, float)) and v > 0:
                    vals.append(float(v))
            except Exception:
                pass
        if vals:
            v = np.array(vals)
            n_unique = len(np.unique(v.round(6)))
            stats[k] = {'n': len(v), 'min': float(v.min()),
                        'max': float(v.max()), 'std': float(v.std()),
                        'unique': n_unique}
            print(f'  {k:40s}  {len(v):>4d}  {v.min():8.4f}  '
                  f'{v.max():8.4f}  {v.std():8.4f}  {n_unique:>6d}', flush=True)
        else:
            print(f'  {k:40s}  (no positive values)', flush=True)

    # Identify candidate constriction-only key
    constr_candidates = [k for k in sigma_keys if 'constr' in k.lower()
                         and 'only' in k.lower()]
    print(f'\n  candidate constriction-only keys: {constr_candidates}',
          flush=True)
    if not constr_candidates:
        print('  ⚠ no constriction-only sigma key — needs to be computed '
              'from raw network output.', flush=True)
    return {'keys': sigma_keys, 'stats': stats,
            'constriction_only_candidates': constr_candidates}


def part2_form_distillation(df):
    """Write out Lasso form explicitly + physical interpretation."""
    print('\n' + '=' * 80, flush=True)
    print('PART 2 — Lasso form distillation (Finding 4 deep)', flush=True)
    print('=' * 80, flush=True)

    # Build features (same as v55 Part A)
    excess = np.maximum(df['phi'].values - 0.20, 1e-6)
    log_excess = np.log(excess)
    log_CN     = np.log(np.maximum(df['cn'].values, 1e-3))
    log_cov    = np.log(np.maximum(df['cov_phys'].values, 1e-3))
    log_f_p    = np.log(np.maximum(df['f_perc'].values, 1e-3))
    log_tau    = np.log(np.maximum(df['tau'].values, 1e-3))
    log_thick  = np.log(np.maximum(df['thickness'].values, 1.0))
    log_gb     = np.log(np.maximum(df['gb_dens'].values, 1e-6))
    porosity   = df['porosity'].values / 100.0

    feats = {
        'log_excess': log_excess, 'log_CN': log_CN,
        'log_cov': log_cov, 'log_f_perc': log_f_p, 'log_tau': log_tau,
        'log_thickness': log_thick, 'log_gb': log_gb,
        'porosity': porosity,
        'log_excess__log_CN': log_excess * log_CN,
        'log_cov__log_f_perc': log_cov * log_f_p,
        'log_tau__log_CN': log_tau * log_CN,
        'log_tau__log_thickness': log_tau * log_thick,
        'log_excess_sq': log_excess ** 2,
        'log_tau_sq': log_tau ** 2,
        'log_CN_sq': log_CN ** 2,
    }
    X = np.column_stack(list(feats.values()))
    names = list(feats.keys())
    Xs = (X - X.mean(0)) / (X.std(0) + 1e-9)
    y = np.log(np.maximum(df['sigma'].values, 1e-12))

    from sklearn.linear_model import LassoCV
    lcv = LassoCV(cv=10, max_iter=20000, n_alphas=120,
                  fit_intercept=True, random_state=42)
    lcv.fit(Xs, y)
    coef = lcv.coef_; intercept = lcv.intercept_

    # Convert standardised coefs back to original units
    # log_y = intercept + Σ (coef_i / std_i) · (X_i - mean_i)
    raw_coef = coef / (X.std(0) + 1e-9)
    raw_intercept = intercept - np.sum(raw_coef * X.mean(0))

    nz = [(names[i], raw_coef[i]) for i in range(len(coef))
          if abs(coef[i]) > 1e-9]
    nz.sort(key=lambda t: -abs(t[1]))
    print('\n  Distilled equation (raw coefficients, log space):', flush=True)
    print(f'    log σ_P = {raw_intercept:+.4f}', flush=True)
    for n_, g_ in nz:
        sign = '+' if g_ >= 0 else '-'
        print(f'              {sign} {abs(g_):.4f} · {n_}', flush=True)

    # Effective exponents
    print('\n  Effective (φ-φc) exponent (varies with CN):', flush=True)
    excess_lc = next((g for n_, g in nz if n_ == 'log_excess'), 0.0)
    excess_lc_sq = next((g for n_, g in nz if n_ == 'log_excess_sq'), 0.0)
    excess_lc_cn = next((g for n_, g in nz if n_ == 'log_excess__log_CN'), 0.0)
    print(f'    base coefs: log_excess={excess_lc:+.4f}  '
          f'log_excess²={excess_lc_sq:+.4f}  log_excess·log_CN={excess_lc_cn:+.4f}',
          flush=True)
    for cn in [3, 4, 5, 6, 8]:
        # ∂log σ / ∂log(φ-φc) = excess_lc + 2*excess_sq*log_excess + excess_cn*log(CN)
        #                     = excess_lc + excess_cn * log(CN)  (linearised)
        eff = excess_lc + excess_lc_cn * np.log(cn)
        print(f'    CN={cn}:  effective exponent ≈ {eff:+.3f}', flush=True)

    print('\n  Effective τ exponent (varies with thickness):', flush=True)
    tau_lc = next((g for n_, g in nz if n_ == 'log_tau'), 0.0)
    tau_sq = next((g for n_, g in nz if n_ == 'log_tau_sq'), 0.0)
    tau_th = next((g for n_, g in nz if n_ == 'log_tau__log_thickness'), 0.0)
    tau_cn = next((g for n_, g in nz if n_ == 'log_tau__log_CN'), 0.0)
    print(f'    base coefs: log_tau={tau_lc:+.4f}  '
          f'log_tau²={tau_sq:+.4f}  log_tau·log_L={tau_th:+.4f}  '
          f'log_tau·log_CN={tau_cn:+.4f}', flush=True)
    for L in [13, 50, 100, 150]:
        eff = tau_lc + tau_th * np.log(L)
        print(f'    L={L}μm:  effective exponent ≈ {eff:+.3f}', flush=True)

    return {'distilled': nz, 'intercept': float(raw_intercept),
            'standardised_coefs': list(coef)}


def part3_penalty_per_batch(df):
    """Stratify plastic penalty by batch."""
    print('\n' + '=' * 80, flush=True)
    print('PART 3 — Plastic penalty per-batch (Finding 2 deep)', flush=True)
    print('=' * 80, flush=True)
    sig_P = np.maximum(df['sigma'].values, 1e-12)
    sig_bulk_H = np.maximum(df['sigma_bulk_H'].values, 1e-6)
    ratio = sig_P / sig_bulk_H

    name = df['name'].astype(str)
    batches = ['1mAh', '6mAh', '8mAh', 'particulate']
    results = {}
    print(f'\n  {"batch":14s}  {"n":>3s}  {"median":>8s}  {"min":>8s}  '
          f'{"max":>8s}  {"σ":>8s}', flush=True)
    for b in batches:
        mask = name.str.contains(b, case=False, na=False).values
        if mask.sum() < 3: continue
        rb = ratio[mask]
        results[b] = {'n': int(mask.sum()),
                      'median': float(np.median(rb)),
                      'min': float(rb.min()),
                      'max': float(rb.max()),
                      'std': float(rb.std()),
                      'mean_phi': float(df[mask]['phi'].mean()),
                      'mean_tau': float(df[mask]['tau'].mean()),
                      'mean_CN': float(df[mask]['cn'].mean())}
        print(f'  {b:14s}  {mask.sum():>3d}  {np.median(rb):8.4f}  '
              f'{rb.min():8.4f}  {rb.max():8.4f}  {rb.std():8.4f}', flush=True)
        print(f'    └─ mean φ={results[b]["mean_phi"]:.3f}  '
              f'τ={results[b]["mean_tau"]:.2f}  CN={results[b]["mean_CN"]:.2f}',
              flush=True)

    # Compare across batches: is penalty driven by batch or by (φ,τ,CN)?
    all_phi = df['phi'].values
    all_cn = df['cn'].values
    feature = np.log(np.maximum(all_phi - 0.20, 1e-6)) * np.log(np.maximum(all_cn, 1e-3))
    # Linear regression of log(ratio) on (φ-φc)·CN feature
    log_r = np.log(ratio)
    fc = feature - feature.mean()
    lc = log_r - log_r.mean()
    slope = float(np.sum(fc * lc) / np.sum(fc ** 2))
    print(f'\n  Single-feature regression: log(ratio) ~ '
          f'log(φ-φc)·log(CN)', flush=True)
    print(f'    slope = {slope:.4f}', flush=True)
    pred = slope * fc + log_r.mean()
    r2 = 1 - np.sum((log_r - pred) ** 2) / np.sum(lc ** 2)
    print(f'    R² = {r2:.4f}', flush=True)
    return results


def part4_universality_0p83(df):
    """Test σ_P = C · σ_H^γ across batches and P:S subsets."""
    print('\n' + '=' * 80, flush=True)
    print('PART 4 — 0.83 universality test (Finding 1 deep)', flush=True)
    print('=' * 80, flush=True)

    log_P = np.log(np.maximum(df['sigma'].values, 1e-12))
    log_H = np.log(np.maximum(df['sigma_H'].values, 1e-6))
    name = df['name'].astype(str)
    p_frac = df['p_frac'].values

    def fit_gamma(mask, label):
        if mask.sum() < 5:
            print(f'  {label:32s}  n={mask.sum()} (too few)', flush=True)
            return None
        x = log_H[mask]; y = log_P[mask]
        x_c = x - x.mean(); y_c = y - y.mean()
        gamma = float(np.sum(x_c * y_c) / np.sum(x_c ** 2))
        intercept = y.mean() - gamma * x.mean()
        pred = gamma * x + intercept
        r2 = 1 - np.sum((y - pred) ** 2) / np.sum(y_c ** 2)
        print(f'  {label:32s}  n={mask.sum():>3d}  γ={gamma:+.4f}  '
              f'R²={r2:.4f}', flush=True)
        return {'n': int(mask.sum()), 'gamma': gamma,
                'intercept': float(intercept), 'r2': float(r2)}

    results = {}
    print('\n  Whole dataset:', flush=True)
    results['all'] = fit_gamma(np.ones(len(df), dtype=bool), 'ALL CASES')

    print('\n  Per-batch:', flush=True)
    for b in ['1mAh', '6mAh', '8mAh', 'particulate']:
        m = name.str.contains(b, case=False, na=False).values
        results[f'batch_{b}'] = fit_gamma(m, b)

    print('\n  Per-P:S ratio:', flush=True)
    ps_buckets = {
        'P:S=5:5 (p=0.5)':    np.abs(p_frac - 0.5) < 0.05,
        'P:S=7:3 (p=0.7)':    np.abs(p_frac - 0.7) < 0.05,
        'P:S=3:7 (p=0.3)':    np.abs(p_frac - 0.3) < 0.05,
        'P:S=10:0 (p=1.0)':   np.abs(p_frac - 1.0) < 0.05,
        'P:S=0:10 (p=0.0)':   np.abs(p_frac - 0.0) < 0.05,
    }
    for label, m in ps_buckets.items():
        results[label] = fit_gamma(m, label)

    # Verdict
    if results['all'] is not None:
        gamma_all = results['all']['gamma']
        per_batch = [r['gamma'] for k, r in results.items()
                     if k.startswith('batch_') and r is not None]
        if per_batch:
            print(f'\n  Mean per-batch γ = {np.mean(per_batch):.3f}, '
                  f'σ = {np.std(per_batch):.3f}', flush=True)
            print(f'  Whole-dataset γ = {gamma_all:.3f}', flush=True)
            if np.std(per_batch) < 0.05:
                print('\n  ✓ γ is BATCH-INVARIANT — strong universality.',
                      flush=True)
            elif np.std(per_batch) < 0.10:
                print('\n  ~ γ moderately consistent across batches.',
                      flush=True)
            else:
                print('\n  ✗ γ varies substantially across batches — '
                      'universality fails.', flush=True)
    return results


def main():
    cases = load_cases()
    rows = enrich_full(load_phys_rows(cases))
    df = pd.DataFrame(rows)
    print(f'Loaded {len(df)} cases.', flush=True)

    # Run all 4 parts
    P1 = part1_sigma_constr_diagnostic()
    P2 = part2_form_distillation(df)
    P3 = part3_penalty_per_batch(df)
    P4 = part4_universality_0p83(df)

    out = Path('docs/figures/physics_regime')
    out.mkdir(parents=True, exist_ok=True)
    save = {'P1_sigma_keys': P1, 'P2_distilled_form': P2,
            'P3_penalty_per_batch': P3, 'P4_universality_gamma': P4}
    with open(out / 'physics_fit_v56_4findings_deep.json', 'w') as f:
        json.dump(save, f, indent=2, default=str)
    print(f'\n→ {out}/physics_fit_v56_4findings_deep.json', flush=True)


if __name__ == '__main__':
    main()
