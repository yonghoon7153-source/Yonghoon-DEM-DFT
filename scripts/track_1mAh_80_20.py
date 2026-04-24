#!/usr/bin/env python3
"""Deep-dive tracer for the 1mAh_80:20 cluster.

The residual_diagnostic flagged 1mAh_80:20 P-rich as +31% distinct (z=2.26σ),
but that used stale hardcoded γ — proper per-run OLS refit showed 1mAh overall
is only +2.5% biased. So the real question is: after correct refit, WHICH
specific 1mAh_80:20 cases are still outliers, and what distinguishes them?

Workflow:
 1. Full joint OLS refit of v32 γ on all cases (same as v32_exhaustive_refit).
 2. Compute err% per case with those fitted γ.
 3. Isolate every case that contains '1mAh' AND am_se_ratio == '80:20'.
 4. Print:
      a) Their residuals, ranked
      b) Their raw metrics + features side-by-side
      c) Peer comparison:
         - Same composition (80:20), different thickness (6mAh, 8mAh)
         - Same mAh class (1mAh), different composition
         - Seed siblings (S1/S2/S3) if present
      d) Feature deltas vs the expected baseline
 5. Verdict: is the cluster explained by any measured feature? If yes, which?

Usage:
  python3 scripts/track_1mAh_80_20.py
"""
from __future__ import annotations
import sys
from pathlib import Path
import numpy as np
import pandas as pd

SCRIPTS = Path(__file__).parent
sys.path.insert(0, str(SCRIPTS))

from v32_exhaustive_refit import (  # noqa: E402
    load_cases, build_features, v29_predict_vec, fit_candidate,
)
from generate_comparison_plots import _formx_v29_params  # noqa: E402


V32_FEATURES = ['LIGG_LB_PCT', 'THIN_X_GEOM', 'P50_DR_DEV', 'PSD_RATIO']


def parse_amse(s):
    if not s or ':' not in str(s):
        return None
    try:
        am, se = map(float, str(s).split(':'))
        return se / (am + se) if (am + se) > 0 else None
    except Exception:
        return None


def main():
    rows = load_cases()
    df = pd.DataFrame(rows).reset_index(drop=True)
    n = len(df)
    print(f'Loaded {n} cases')

    # Inject am_se_ratio from full_metrics if present (load_cases doesn't pull it)
    amse_list = []
    for _, r in df.iterrows():
        # Try to get am_se_ratio from the webapp archive
        cid = r['case_id']
        import json
        amse = None
        for p in (Path('webapp/archive').rglob(f'{cid}/full_metrics.json')):
            try:
                m = json.load(open(p))
                amse = m.get('am_se_ratio')
            except Exception:
                pass
            break
        amse_list.append(amse)
    df['am_se_ratio'] = amse_list

    # ── Full v32 joint fit ──────────────────────────────────────
    params = _formx_v29_params()
    base_pred = v29_predict_vec(df, params)
    features = build_features(df)
    res_v32 = fit_candidate(df, V32_FEATURES, features, base_pred)
    df['sigma_v32'] = res_v32['pred']
    df['err_pct'] = (df['sigma_actual'] - df['sigma_v32']) / df['sigma_v32'] * 100

    print(f'\n=== v32 joint refit ===')
    print(f'  R² = {res_v32["r2"]:.4f}   LOOCV = {res_v32["loocv"]:.4f}   w20 = {res_v32["w20"]}/{n}')
    print(f'  γ values: ' + ', '.join(f'{f}={g:+.3f}'
                                      for f, g in zip(V32_FEATURES, res_v32['gammas'])))

    # ── Isolate 1mAh + 80:20 cluster ─────────────────────────────
    is_1mAh = df['name'].str.lower().str.contains('1mah|thin', regex=True).values
    is_80_20 = df['am_se_ratio'] == '80:20'
    cluster = df[is_1mAh & is_80_20].copy().sort_values('err_pct', ascending=False)

    print(f'\n=== 1mAh ∧ 80:20 cluster ({len(cluster)} cases) ===')
    cols = ['name', 'thick', 'porosity', 'phi', 'cn', 'tau',
            'cov', 'p_frac', 'sigma_actual', 'sigma_v32', 'err_pct']
    with pd.option_context('display.max_rows', None, 'display.width', 180,
                           'display.float_format', lambda x: f'{x:6.3f}' if abs(x) < 1000 else f'{x:7.1f}'):
        print(cluster[cols].to_string(index=False))

    # ── Peer groups for contrast ─────────────────────────────────
    # Peer A: other AM:SE at 1mAh (different composition, same thickness class)
    # Peer B: 80:20 at thicker mAh (6mAh, 8mAh) — should isolate thickness effect
    is_other_amse_1mAh = is_1mAh & (df['am_se_ratio'] != '80:20') & df['am_se_ratio'].notna()
    is_80_20_thick = (~is_1mAh) & (df['am_se_ratio'] == '80:20')

    peerA = df[is_other_amse_1mAh].sort_values('err_pct', ascending=False)
    peerB = df[is_80_20_thick].sort_values('err_pct', ascending=False)

    def summarise(label, grp):
        if len(grp) == 0:
            print(f'  {label}: no cases')
            return
        errs = grp['err_pct'].values
        print(f'  {label}: n={len(grp)}  mean={errs.mean():+.2f}  median={np.median(errs):+.2f}  '
              f'std={errs.std():.2f}  range=[{errs.min():+.1f}, {errs.max():+.1f}]')

    print(f'\n=== PEER SUMMARY (err%) ===')
    summarise('1mAh ∧ 80:20 (target)   ', cluster)
    summarise('1mAh ∧ ¬80:20 (other AMSE)', peerA)
    summarise('¬1mAh ∧ 80:20 (thick 80:20)', peerB)
    summarise('ALL CASES                ', df)

    # ── Feature contrast: cluster vs peers ────────────────────────
    feat_cols = ['thick', 'porosity', 'phi', 'cn', 'tau', 'cov', 'p_frac']
    print(f'\n=== FEATURE MEANS (cluster vs peer A vs peer B) ===')
    print(f'{"feature":10s}  {"cluster":>10s}  {"peerA(1mAh)":>12s}  {"peerB(80:20 thick)":>18s}  {"ALL":>8s}')
    for fc in feat_cols:
        c = cluster[fc].mean() if len(cluster) else float('nan')
        a = peerA[fc].mean() if len(peerA) else float('nan')
        b = peerB[fc].mean() if len(peerB) else float('nan')
        al = df[fc].mean()
        print(f'{fc:10s}  {c:10.3f}  {a:12.3f}  {b:18.3f}  {al:8.3f}')

    # ── Within-cluster residual feature scan ─────────────────────
    if len(cluster) >= 3:
        print(f'\n=== WITHIN-CLUSTER: residual vs feature (n={len(cluster)}) ===')
        cerr = cluster['err_pct'].values
        for fc in feat_cols:
            xs = cluster[fc].values
            if np.std(xs) == 0:
                continue
            r = float(np.corrcoef(xs, cerr)[0, 1])
            if abs(r) > 0.3:
                print(f'  {fc:10s}  r={r:+.3f}   ← notable')
            else:
                print(f'  {fc:10s}  r={r:+.3f}')

    # ── Seed-siblings analysis ────────────────────────────────────
    # Find cases that share a stem (e.g. input_1mAh_6 base + input_1mAh_6_S{1,2,3})
    print(f'\n=== SEED SIBLINGS (1mAh_80:20 only) ===')
    cluster_names = cluster['name'].tolist()
    stems = {}
    for nm in cluster_names:
        # Strip _S\d suffix if present
        base = nm
        for suf in ('_S1', '_S2', '_S3'):
            if base.endswith(suf):
                base = base[:-len(suf)]
                break
        stems.setdefault(base, []).append(nm)
    for base, siblings in stems.items():
        if len(siblings) < 2:
            continue
        sibling_rows = cluster[cluster['name'].isin(siblings)]
        errs = sibling_rows['err_pct'].values
        print(f'  {base} [{",".join(siblings)}]:')
        print(f'    err% = {errs}  → mean={errs.mean():+.2f}  std={errs.std():.2f}')

    # ── Verdict ──────────────────────────────────────────────────
    if len(cluster) == 0:
        print('\n=== VERDICT ===')
        print('  No 1mAh_80:20 cases found.')
        return
    c_errs = cluster['err_pct'].values
    all_errs = df['err_pct'].values
    z = (c_errs.mean() - all_errs.mean()) / (all_errs.std() + 1e-9) * np.sqrt(len(cluster))
    print(f'\n=== VERDICT ===')
    print(f'  Cluster mean err: {c_errs.mean():+.2f}%  (global {all_errs.mean():+.2f}%)')
    print(f'  Cluster std:      {c_errs.std():.2f}%   (global {all_errs.std():.2f}%)')
    print(f'  z-score vs global: {z:+.2f}σ')
    if abs(z) > 2:
        print(f'  → CLUSTER still distinct after proper refit. Worth Methods note.')
    elif abs(z) > 1:
        print(f'  → Mild deviation. Likely within seed noise.')
    else:
        print(f'  → Within normal scatter. The residual_diagnostic signal was a refit artifact.')


if __name__ == '__main__':
    main()
