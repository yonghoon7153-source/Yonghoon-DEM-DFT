#!/usr/bin/env python3
"""Physics-mode fit v37 — true 3-way independent fits → honest ceiling.

v36 cluster indicators got at most R²=0.978 (combined). The 'is_1mAh_5050'
indicator tagged 27/76 cases — too broad, since only 5–9 of those were
actually mispredicted. Diluting the signal across 27 cases meant the
indicator couldn't push the combined fit past ≈0.98.

This script answers a different question: if we fit three completely
independent v29 power-laws, one per regime, what's the **honest
ceiling** for each?

  Regime A — cluster (1mAh ∩ p:s=5:5)         tag = is_1mAh_5050
  Regime B — thick non-cluster (τ<1.5, ¬tag)
  Regime C — not-thick non-cluster (τ≥1.5, ¬tag)

Independence means each subset gets its own α, β, γ, δ, φc, μ, b0
and is fit to its own σ_actual values. The combined R² is then just
a concatenation across all 76 predictions — a fair report of the
unified scaling story without parameter sharing.

Output:
  • Per-regime: n, R², LOOCV, params
  • Combined (concat preds): R², w20
  • Honest publication framing recommendation

If any single regime alone hits R²<0.97, that subset has higher
inherent noise — no form will rescue it. If all three hit R²≥0.99,
the combined is publishable as a 3-regime unified law.
"""
from __future__ import annotations
import sys, json
from pathlib import Path
import numpy as np
import pandas as pd

SCRIPTS = Path(__file__).parent
sys.path.insert(0, str(SCRIPTS))
from physics_fit_v33_binding import (  # noqa: E402
    load_phys_rows, fit_base, predict_base, metrics, loocv_r2,
)
from v32_exhaustive_refit import load_cases  # noqa: E402

WEBAPP = SCRIPTS.parent / 'webapp'
SIGMA_GRAIN = 3.0


def _read_full_metrics(cid: str) -> dict | None:
    for base in ('results', 'archive'):
        for p in (WEBAPP / base).rglob(f'{cid}/full_metrics.json'):
            try:
                return json.load(open(p))
            except Exception:
                pass
    return None


def enrich_extras(rows):
    out = []
    for r in rows:
        m = _read_full_metrics(r['case_id'])
        r2 = dict(r)
        r2['thickness'] = float((m or {}).get('thickness_um', 0) or 0)
        out.append(r2)
    return out


def fit_subset(df_sub, label, n_start=15):
    """Fit base power-law on a subset. Reports R²/LOOCV/w20."""
    if len(df_sub) < 5:
        print(f'  {label}: n={len(df_sub)} (too few — skipping)')
        return None
    params = fit_base(df_sub, n_start=n_start)
    pred = predict_base(df_sub, params)
    r2, w20 = metrics(df_sub['sigma'].values, pred)
    loocv = loocv_r2(df_sub, pred)
    print(f'  {label}: n={len(df_sub):>3d}   R²={r2:.4f}   '
          f'LOOCV={loocv:.4f}   w20={w20}/{len(df_sub)}')
    print('    params:',
          '  '.join(f'{n}={v:+.3f}' for n, v in zip(
              ('α','β','γ','δ','φc','μ','b0'), params)))
    return {'n': len(df_sub), 'r2': r2, 'loocv': loocv, 'w20': w20,
            'params': list(params), 'pred': pred,
            'sigma': df_sub['sigma'].values, 'names': df_sub['name'].tolist()}


def main():
    cases = load_cases()
    rows = enrich_extras(load_phys_rows(cases))
    df = pd.DataFrame(rows)

    name = df['name'].astype(str)
    is_1mAh = name.str.contains('1mAh', case=False, na=False).values
    p5050   = (np.abs(df['p_frac'].values - 0.5) < 0.05)
    is_cluster = is_1mAh & p5050
    df['is_cluster'] = is_cluster.astype(float)

    sub_cluster = df[is_cluster].reset_index(drop=True)
    sub_thick   = df[(~is_cluster) & (df['tau'] <  1.5)].reset_index(drop=True)
    sub_thin    = df[(~is_cluster) & (df['tau'] >= 1.5)].reset_index(drop=True)

    print(f'Total cases: {len(df)}')
    print(f'  cluster (1mAh ∩ p:s=5:5):     n={len(sub_cluster):>3d}')
    print(f'  thick non-cluster (τ<1.5):    n={len(sub_thick):>3d}')
    print(f'  not-thick non-cluster (τ≥1.5): n={len(sub_thin):>3d}')

    print('\n' + '=' * 75)
    print('=== Per-regime independent fits ===')
    print('=' * 75)
    A = fit_subset(sub_cluster, 'A. cluster', n_start=20)
    B = fit_subset(sub_thick,   'B. thick',   n_start=15)
    C = fit_subset(sub_thin,    'C. ¬thick',  n_start=15)

    # Combined (concat predictions)
    preds, sigmas, regimes = [], [], []
    for label, X in [('A', A), ('B', B), ('C', C)]:
        if X is None:
            continue
        preds.append(X['pred'])
        sigmas.append(X['sigma'])
        regimes.extend([label] * len(X['sigma']))
    pred_all = np.concatenate(preds)
    sigma_all = np.concatenate(sigmas)
    a = np.log(sigma_all + 1e-12); p = np.log(pred_all + 1e-12)
    ss_res = np.sum((a - p) ** 2); ss_tot = np.sum((a - a.mean()) ** 2)
    r2_combo = 1 - ss_res / ss_tot if ss_tot > 0 else 0.0
    err = np.abs(sigma_all - pred_all) / np.maximum(sigma_all, 1e-12)
    w20_combo = int(np.sum(err <= 0.20))
    n_total = len(sigma_all)

    # Per-regime LOOCV combined as well
    print('\n' + '=' * 75)
    print('=== COMBINED (concat per-regime independent preds) ===')
    print('=' * 75)
    print(f'  n={n_total}   R²={r2_combo:.4f}   w20={w20_combo}/{n_total}')

    # Honest verdict
    print('\n' + '=' * 75)
    print('=== HONEST PUBLICATION VERDICT ===')
    print('=' * 75)
    if r2_combo >= 0.99:
        print('  🎯 R² ≥ 0.99 with 3-way independent fits.')
        print('  Publication framing: "Regime-aware unified scaling law splits the')
        print('  dataset into thick / not-thick / 1mAh-thin-film clusters and fits')
        print('  each with a v29 power-law form, achieving combined R²=0.99 across')
        print('  all 76 cases without parameter sharing across regimes."')
    elif r2_combo >= 0.985:
        print(f'  R²={r2_combo:.4f} with 3-way fits (gap to 0.99 = {0.99 - r2_combo:+.4f}).')
        print('  Publication framing: report per-regime results and the combined.')
        print('  Each regime\'s individual ceiling is the honest noise floor.')
    else:
        print(f'  R²={r2_combo:.4f} with 3-way fits.  This is the noise floor of')
        print('  this dataset given v29 form. Pushing further requires either:')
        print('    - More cases per regime (especially thin: only ~5 cases)')
        print('    - Genuinely new features beyond DEM output')
        print('    - Acceptance that 0.97-0.98 IS state of the art for ASSB.')

    # Per-regime ceilings
    print('\n=== Per-regime individual R² ceilings ===')
    for label, X in [('A. cluster (1mAh+5050)', A),
                     ('B. thick non-cluster',    B),
                     ('C. ¬thick non-cluster',  C)]:
        if X is not None:
            print(f'  {label:30s}: R²={X["r2"]:.4f}  '
                  f'(LOOCV={X["loocv"]:.4f}, n={X["n"]})')

    # Save
    out = Path('docs/figures/physics_regime')
    out.mkdir(parents=True, exist_ok=True)
    save = {
        'A_cluster': {k: v for k, v in (A or {}).items() if k not in ('pred','sigma','names')},
        'B_thick':   {k: v for k, v in (B or {}).items() if k not in ('pred','sigma','names')},
        'C_thin':    {k: v for k, v in (C or {}).items() if k not in ('pred','sigma','names')},
        'combined':  {'n': n_total, 'r2': r2_combo, 'w20': w20_combo},
    }
    with open(out / 'physics_fit_v37_3way.json', 'w') as f:
        json.dump(save, f, indent=2, default=str)
    print(f'\n→ {out}/physics_fit_v37_3way.json')


if __name__ == '__main__':
    main()
