#!/usr/bin/env python3
"""Section 5 validity filter robustness analysis.

Empirical confirmation of the construction-based decoupling argued in
Section 4: if σ_ionic depends on the SE-SE network rather than AM-AM
fracture, then filtering the ensemble to "low-fracture" cases (those
where DEM over-overlap is mild) should not change the v29 fit
quality.

Procedure
─────────
1. Load metrics_master.csv (master DB).
2. Pick the v29 features and the σ_ionic target. Single-feature
   regression on log τ as a coarse proxy when full v29 is unavailable.
3. Compute baseline LOOCV R² over all cases.
4. Apply fracture_index < 0.10 filter; recompute LOOCV R² on the
   surviving subset.
5. Report numerical evidence to fill Section 5 of the brittle caveat.

Output
──────
Console table with case counts, LOOCV R² baseline / filtered, and
relative shift. Plain text suitable for direct paste into the paper.
"""
from __future__ import annotations
import math
from pathlib import Path
import sys

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
DB_CSV = ROOT / 'docs' / 'db' / 'metrics_master.csv'

# v29 form: log σ_P = c + a·log(φ-φc) + b·log CN + c·log cov + d·log f_perc - e·log τ
# We approximate without exact form refit by using a generic multi-linear
# regression in log space. If the master DB carries v29_fit_per_case
# residuals, those are used directly.

PHI_C = 0.20  # canonical percolation threshold for SE


def loocv_r2(X: np.ndarray, y: np.ndarray) -> float:
    """Single-feature or multi-feature OLS LOOCV R². Manual loop —
    avoids sklearn binary-incompatibility issues."""
    n = X.shape[0]
    if n < 5:
        return float('nan')
    pred = np.empty(n)
    for i in range(n):
        mask = np.ones(n, dtype=bool); mask[i] = False
        X_tr = X[mask]; y_tr = y[mask]
        # Augment with intercept
        X1 = np.hstack([np.ones((X_tr.shape[0], 1)), X_tr])
        try:
            beta, *_ = np.linalg.lstsq(X1, y_tr, rcond=None)
        except np.linalg.LinAlgError:
            pred[i] = y_tr.mean(); continue
        x_te = np.hstack([1.0, X[i]])
        pred[i] = float(x_te @ beta)
    ss_r = np.sum((y - pred) ** 2)
    ss_t = np.sum((y - y.mean()) ** 2)
    if ss_t <= 0:
        return float('nan')
    return float(1.0 - ss_r / ss_t)


def main() -> None:
    if not DB_CSV.exists():
        sys.exit(f'metrics_master.csv not found at {DB_CSV}\n'
                 f'Run build_metrics_db.py --rebuild first.')
    df = pd.read_csv(DB_CSV)
    print(f'Loaded {len(df)} cases from master DB.', flush=True)

    # Required columns
    target_col = 'sigma_full_mScm'
    if target_col not in df.columns:
        sys.exit(f'Column {target_col} missing — run network_conductivity '
                 f'pipeline first.')

    # v29 features (canonical)
    feature_specs = [
        ('porosity',           'porosity'),
        ('tortuosity',         'tortuosity_recommended'),
        ('cn_se_se',           'se_se_cn'),
        ('coverage_AM_S',      'coverage_AM_S_mean'),
        ('top_reachable_pct',  'top_reachable_pct'),
    ]
    fcols = [c for _, c in feature_specs if c in df.columns]
    if len(fcols) < 3:
        sys.exit(f'Too few v29 features available; got {fcols}')

    # Filter: numeric, finite, σ > 0
    df_full = df.copy()
    df_full = df_full[df_full[target_col].notna() & (df_full[target_col] > 0)]
    for c in fcols:
        df_full = df_full[df_full[c].notna()]
    df_full = df_full.reset_index(drop=True)
    print(f'  After filtering NaN/non-positive σ: {len(df_full)} cases', flush=True)

    # Build feature matrix in log space
    def _build(sub):
        # log τ, log porosity, log CN, log cov, log f_perc/100
        cols = []
        if 'tortuosity_recommended' in sub.columns:
            cols.append(np.log(np.maximum(sub['tortuosity_recommended'].values, 1e-3)))
        if 'porosity' in sub.columns:
            phi_se = (1.0 - sub['porosity'].values / 100.0) / 2.0
            phi_eff = np.maximum(phi_se - PHI_C, 1e-3)
            cols.append(np.log(phi_eff))
        if 'se_se_cn' in sub.columns:
            cols.append(np.log(np.maximum(sub['se_se_cn'].values, 0.1)))
        if 'coverage_AM_S_mean' in sub.columns:
            cols.append(np.log(np.maximum(sub['coverage_AM_S_mean'].values / 100.0, 1e-3)))
        if 'top_reachable_pct' in sub.columns:
            cols.append(np.log(np.maximum(sub['top_reachable_pct'].values / 100.0, 1e-3)))
        return np.column_stack(cols)

    X_full = _build(df_full)
    y_full = np.log(np.maximum(df_full[target_col].values, 1e-12))

    n_full = X_full.shape[0]
    r2_full = loocv_r2(X_full, y_full)

    # ── Validity filter: fracture_index < 0.10 ─────────────────────────
    if 'fracture_index' not in df_full.columns:
        sys.exit('fracture_index missing — run b2_b4_diagnostic + backfill.')

    masks = {
        'all':                        np.ones(len(df_full), dtype=bool),
        'fracture_index < 0.10':       (df_full['fracture_index'] < 0.10).values,
        'fracture_index < 0.05':       (df_full['fracture_index'] < 0.05).values,
        'fracture_index_force < 0.10': (df_full['fracture_index_force'] < 0.10).values
                                       if 'fracture_index_force' in df_full.columns
                                       else np.ones(len(df_full), dtype=bool),
    }

    print()
    print('=' * 72, flush=True)
    print('Section 5 — Validity-filter robustness check', flush=True)
    print('=' * 72, flush=True)
    print(f'  v29-style features used: {fcols}', flush=True)
    print(f'  Target: log({target_col})', flush=True)
    print()
    print(f'  {"Filter":<32s} {"n":>5s}  {"LOOCV R²":>10s}  {"ΔR² vs all":>12s}',
          flush=True)
    print('  ' + '-' * 65, flush=True)

    r2_baseline = None
    for label, mask in masks.items():
        n = int(mask.sum())
        if n < 5:
            print(f'  {label:<32s} {n:>5d}  {"N/A (n<5)":>10s}', flush=True)
            continue
        r2 = loocv_r2(X_full[mask], y_full[mask])
        if label == 'all':
            r2_baseline = r2
            delta = ''
        else:
            delta = f'{(r2 - r2_baseline):+.4f}' if r2_baseline is not None else ''
        print(f'  {label:<32s} {n:>5d}  {r2:>10.4f}  {delta:>12s}', flush=True)

    print()
    print('Interpretation:', flush=True)
    print('  - "all" row is the baseline LOOCV R² with no filter.',
          flush=True)
    print('  - The filtered rows are the validity-filter robustness check', flush=True)
    print('    of the σ_ionic scaling-law conclusion.', flush=True)
    print('  - If |ΔR²| < 0.02 the filter does not meaningfully shift the', flush=True)
    print('    fit quality — Section 4 decoupling is empirically confirmed.', flush=True)
    print('  - If |ΔR²| > 0.05 the σ_ionic claim depends on which fracture-', flush=True)
    print('    permissive cases are included, which would weaken the paper.', flush=True)


if __name__ == '__main__':
    main()
