#!/usr/bin/env python3
"""Omnidirectional ("전방위") interaction map on the master metric CSV.

For EVERY response, fit a standardized OLS on the full term set of the three
design knobs — main effects + pairwise interactions + quadratics:

    phi_se, r_SE, p_frac,
    phi_se², p_frac²,                         (curvature → captures the Furnas dip)
    phi_se×r_SE, phi_se×p_frac, r_SE×p_frac   (interactions)

Outputs docs/figures/interaction_matrix.png:
  • LEFT  — β matrix: responses (rows) × terms (cols), standardized coefficient
            (RdBu); each row labelled with its R² and n.  One glance = which
            knob / interaction / curvature drives which response.
  • RIGHT — response↔response Spearman correlation (how the outcomes co-move).
And prints the full per-response coefficient table + the dominant term.

  python3 scripts/interaction_matrix.py [--csv docs/data/case_master.csv]
"""
import argparse
import numpy as np
import pandas as pd

KNOBS = ['phi_se', 'r_SE', 'p_frac']
# (label, builder over standardized knob dict Z)
TERMS = [
    ('phi_se',        lambda Z: Z['phi_se']),
    ('r_SE',          lambda Z: Z['r_SE']),
    ('p_frac',        lambda Z: Z['p_frac']),
    ('phi_se^2',      lambda Z: Z['phi_se'] ** 2),
    ('p_frac^2',      lambda Z: Z['p_frac'] ** 2),
    ('phi_se×r_SE',   lambda Z: Z['phi_se'] * Z['r_SE']),
    ('phi_se×p_frac', lambda Z: Z['phi_se'] * Z['p_frac']),
    ('r_SE×p_frac',   lambda Z: Z['r_SE'] * Z['p_frac']),
]
# response col -> (display label, log10?)
RESP = [
    ('porosity',                   'porosity DEM',  False),
    ('mpm.porosity_mpm_pct',       'porosity MPM',  False),
    ('thickness_um',               'thickness',     False),
    ('overlap_fraction_pct',       'overlap',       False),
    ('sigma_full_mScm',            'σ_ionic',       True),
    ('electronic_sigma_full_mScm', 'σ_e',           True),
    ('thermal_sigma_full_mScm',    'κ',             True),
    ('se_se_cn',                   'SE-SE CN',      False),
    ('am_am_cn',                   'AM-AM CN',      False),
    ('coverage_AM_P_mean',         'cov_AM_P',      False),
    ('tortuosity_mean',            'τ',             False),
    ('fracture_index',             'fracture',      False),
]


def fit(df, ycol, logy):
    d = df[[ycol] + KNOBS].apply(pd.to_numeric, errors='coerce').dropna()
    if len(d) < len(TERMS) + 3:
        return None, None, len(d)
    Y = np.log10(d[ycol].clip(lower=1e-6)) if logy else d[ycol].values.astype(float)
    Y = (Y - Y.mean()) / (Y.std() or 1)
    Z = {k: (d[k].values - d[k].values.mean()) / (d[k].values.std() or 1) for k in KNOBS}
    cols = [b(Z) for _, b in TERMS]
    X = np.column_stack([np.ones(len(d))] + cols)
    beta, *_ = np.linalg.lstsq(X, Y, rcond=None)
    r2 = 1 - ((Y - X @ beta) ** 2).sum() / (((Y - Y.mean()) ** 2).sum() or 1)
    return dict(zip([t for t, _ in TERMS], beta[1:])), r2, len(d)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--csv', default='docs/data/case_master.csv')
    ap.add_argument('--out', default='docs/figures/interaction_matrix.png')
    a = ap.parse_args()
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt

    df = pd.read_csv(a.csv)

    rows, B, R2, N = [], [], [], []
    print('=== per-response standardized OLS (main + interaction + quadratic) ===')
    for col, lab, logy in RESP:
        if col not in df.columns:
            continue
        coef, r2, n = fit(df, col, logy)
        if coef is None:
            print(f'  {lab:14s} skipped (n={n} too few)')
            continue
        rows.append(f'{lab}  (R²={r2:.2f}, n={n})')
        B.append([coef[t] for t, _ in TERMS]); R2.append(r2); N.append(n)
        dom = max(coef.items(), key=lambda kv: abs(kv[1]))
        print(f'\n{lab}{" (log)" if logy else ""}  R²={r2:.3f} n={n}  ▶ dominant: {dom[0]} ({dom[1]:+.2f})')
        for t, b in sorted(coef.items(), key=lambda kv: -abs(kv[1])):
            if abs(b) > 0.12:
                print(f'    {t:16s} {b:+.3f} ★')

    B = np.array(B)
    fig, (axL, axR) = plt.subplots(1, 2, figsize=(19, 8),
                                   gridspec_kw={'width_ratios': [1.35, 1]})

    # LEFT — β interaction matrix
    vmax = np.nanpercentile(np.abs(B), 98) or 1
    im = axL.imshow(B, cmap='RdBu_r', vmin=-vmax, vmax=vmax, aspect='auto')
    axL.set_xticks(range(len(TERMS))); axL.set_xticklabels([t for t, _ in TERMS], rotation=45, ha='right', fontsize=9)
    axL.set_yticks(range(len(rows))); axL.set_yticklabels(rows, fontsize=8)
    for i in range(B.shape[0]):
        for j in range(B.shape[1]):
            v = B[i, j]
            if not np.isnan(v):
                axL.text(j, i, f'{v:+.2f}', ha='center', va='center', fontsize=6.5,
                         color='white' if abs(v) > vmax * 0.6 else 'black')
    # gridline separating main effects | quadratics | interactions
    axL.axvline(2.5, color='k', lw=1.2); axL.axvline(4.5, color='k', lw=1.2)
    axL.set_title('standardized β  —  response (row) × knob term (col)\n'
                  '|  main effects  |  curvature  |  interactions  |', fontsize=10)
    fig.colorbar(im, ax=axL, fraction=0.046, label='β (standardized)')

    # RIGHT — response↔response Spearman correlation
    rc = [c for c, _, _ in RESP if c in df.columns]
    rl = [l for c, l, _ in RESP if c in df.columns]
    C = df[rc].apply(pd.to_numeric, errors='coerce').corr(method='spearman')
    im2 = axR.imshow(C.values, cmap='PuOr_r', vmin=-1, vmax=1, aspect='auto')
    axR.set_xticks(range(len(rl))); axR.set_xticklabels(rl, rotation=45, ha='right', fontsize=8)
    axR.set_yticks(range(len(rl))); axR.set_yticklabels(rl, fontsize=8)
    for i in range(len(rl)):
        for j in range(len(rl)):
            v = C.values[i, j]
            if not np.isnan(v):
                axR.text(j, i, f'{v:.2f}', ha='center', va='center', fontsize=6,
                         color='white' if abs(v) > 0.6 else 'black')
    axR.set_title('response ↔ response (Spearman)', fontsize=10)
    fig.colorbar(im2, ax=axR, fraction=0.046)

    fig.suptitle(f'Omnidirectional interaction map — {len(df)} cases  '
                 f'(knobs: φ_SE, r_SE, p_frac)', fontsize=13)
    import os
    os.makedirs(os.path.dirname(a.out) or '.', exist_ok=True)
    fig.tight_layout(rect=[0, 0, 1, 0.96]); fig.savefig(a.out, dpi=130)
    print(f'\nsaved {a.out}')


if __name__ == '__main__':
    main()
