#!/usr/bin/env python3
"""Interaction analysis on the master metric CSV (163 cases × 421 cols).

Design knobs:  phi_se (SE volume fraction = composition), r_SE (SE radius),
               p_frac (AM_P fraction of the AM = P:S).
Responses:     porosity (DEM), mpm.porosity_mpm_pct (MPM), sigma_full_mScm
               (σ_ionic), electronic/thermal σ, se_se_cn, coverage, tortuosity,
               fracture.

Produces docs/figures/master_interactions.png (corr heatmap + key interaction
scatters + DEM↔MPM parity + standardized-OLS interaction-coefficient bars) and
prints an OLS-with-interactions table (numpy lstsq; σ in log10).  The headline
question: which INTERACTION (esp. r_SE × p_frac, phi_se × p_frac) drives the
porosity dip and the σ_ionic percolation collapse.

  python3 scripts/analyze_master_interactions.py [--csv docs/data/case_master.csv]
"""
import argparse
import numpy as np
import pandas as pd


def _num(df, c):
    return pd.to_numeric(df[c], errors='coerce') if c in df.columns else pd.Series(np.nan, index=df.index)


def ols_interactions(df, y, knobs, logy=False):
    """Standardized OLS y ~ knobs + all pairwise interactions. Returns (coef dict, R2, n)."""
    d = df[[y] + knobs].apply(pd.to_numeric, errors='coerce').dropna()
    if len(d) < len(knobs) * 3 + 3:
        return None, None, len(d)
    Y = np.log10(d[y].clip(lower=1e-6)) if logy else d[y].values.astype(float)
    Y = (Y - Y.mean()) / (Y.std() or 1)
    cols, names = [], []
    Z = {k: (d[k].values - d[k].values.mean()) / (d[k].values.std() or 1) for k in knobs}
    for k in knobs:
        cols.append(Z[k]); names.append(k)
    for i in range(len(knobs)):
        for j in range(i + 1, len(knobs)):
            cols.append(Z[knobs[i]] * Z[knobs[j]]); names.append(f'{knobs[i]}×{knobs[j]}')
    X = np.column_stack([np.ones(len(d))] + cols)
    beta, *_ = np.linalg.lstsq(X, Y, rcond=None)
    yhat = X @ beta
    r2 = 1 - ((Y - yhat) ** 2).sum() / ((Y - Y.mean()) ** 2).sum()
    return dict(zip(names, beta[1:])), r2, len(d)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--csv', default='docs/data/case_master.csv')
    ap.add_argument('--out', default='docs/figures/master_interactions.png')
    a = ap.parse_args()
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt

    df = pd.read_csv(a.csv)
    # am_wt from "82:18" string (first number = AM wt%)
    df['am_wt'] = df['am_se_ratio'].astype(str).str.extract(r'^\s*(\d+(?:\.\d+)?)\s*:')[0].astype(float)

    KNOBS = ['phi_se', 'r_SE', 'p_frac']
    RESP = {'porosity': 'porosity (DEM %)', 'mpm.porosity_mpm_pct': 'porosity (MPM %)',
            'sigma_full_mScm': 'σ_ionic', 'electronic_sigma_full_mScm': 'σ_e',
            'thermal_sigma_full_mScm': 'κ', 'se_se_cn': 'SE-SE CN',
            'coverage_AM_P_mean': 'cov_AM_P', 'tortuosity_mean': 'τ',
            'fracture_index': 'fracture'}
    RESP = {k: v for k, v in RESP.items() if k in df.columns}

    fig = plt.figure(figsize=(18, 11))
    gs = fig.add_gridspec(2, 3, hspace=0.32, wspace=0.30)

    # ── A: correlation heatmap (Spearman, robust to the σ order-of-mag spread) ──
    axA = fig.add_subplot(gs[0, 0])
    hm_cols = KNOBS + list(RESP)
    M = df[hm_cols].apply(pd.to_numeric, errors='coerce')
    C = M.corr(method='spearman')
    im = axA.imshow(C.values, cmap='RdBu_r', vmin=-1, vmax=1)
    lbls = KNOBS + [RESP[k] for k in RESP]
    axA.set_xticks(range(len(lbls))); axA.set_xticklabels(lbls, rotation=90, fontsize=7)
    axA.set_yticks(range(len(lbls))); axA.set_yticklabels(lbls, fontsize=7)
    for i in range(len(lbls)):
        for j in range(len(lbls)):
            v = C.values[i, j]
            if not np.isnan(v):
                axA.text(j, i, f'{v:.2f}', ha='center', va='center', fontsize=5.5,
                         color='white' if abs(v) > 0.6 else 'black')
    axA.set_title('Spearman correlation (knobs ↔ responses)', fontsize=9)
    fig.colorbar(im, ax=axA, fraction=0.046)

    # ── B: porosity(DEM) vs phi_se, colored by r_SE ──
    axB = fig.add_subplot(gs[0, 1])
    d = df[['phi_se', 'porosity', 'r_SE']].apply(pd.to_numeric, errors='coerce').dropna()
    sc = axB.scatter(d['phi_se'], d['porosity'], c=d['r_SE'], cmap='viridis', s=28, alpha=0.8)
    axB.set_xlabel('φ_SE (SE volume fraction)'); axB.set_ylabel('porosity DEM (%)')
    axB.set_title('porosity ↓ as φ_SE ↑ (SE fills voids)', fontsize=9)
    fig.colorbar(sc, ax=axB, label='r_SE (µm)', fraction=0.046)
    axB.grid(alpha=0.3)

    # ── C: porosity(DEM) vs p_frac, colored by phi_se — the Furnas dip ──
    axC = fig.add_subplot(gs[0, 2])
    d = df[['p_frac', 'porosity', 'phi_se', 'r_SE']].apply(pd.to_numeric, errors='coerce').dropna()
    sc = axC.scatter(d['p_frac'], d['porosity'], c=d['phi_se'], cmap='plasma', s=28, alpha=0.85)
    axC.set_xlabel('p_frac (AM_P fraction, P:S)'); axC.set_ylabel('porosity DEM (%)')
    axC.set_title('Furnas dip vs P:S (color = φ_SE)', fontsize=9)
    fig.colorbar(sc, ax=axC, label='φ_SE', fraction=0.046)
    axC.grid(alpha=0.3)

    # ── D: log σ_ionic vs phi_se, colored by r_SE — percolation collapse ──
    axD = fig.add_subplot(gs[1, 0])
    d = df[['phi_se', 'sigma_full_mScm', 'r_SE']].apply(pd.to_numeric, errors='coerce').dropna()
    d = d[d['sigma_full_mScm'] > 0]
    sc = axD.scatter(d['phi_se'], np.log10(d['sigma_full_mScm']), c=d['r_SE'], cmap='viridis', s=28, alpha=0.8)
    axD.set_xlabel('φ_SE'); axD.set_ylabel('log₁₀ σ_ionic (mS/cm)')
    axD.set_title('σ_ionic percolation collapse at low φ_SE', fontsize=9)
    fig.colorbar(sc, ax=axD, label='r_SE (µm)', fraction=0.046)
    axD.grid(alpha=0.3)

    # ── E: DEM vs MPM porosity parity (cases with MPM) ──
    axE = fig.add_subplot(gs[1, 1])
    d = df[['porosity', 'mpm.porosity_mpm_pct', 'phi_se']].apply(pd.to_numeric, errors='coerce').dropna()
    lo, hi = 0, max(d['porosity'].max(), d['mpm.porosity_mpm_pct'].max()) + 2
    axE.plot([lo, hi], [lo, hi], 'k--', lw=1)
    sc = axE.scatter(d['porosity'], d['mpm.porosity_mpm_pct'], c=d['phi_se'], cmap='plasma', s=30)
    axE.set_xlabel('porosity DEM (%)'); axE.set_ylabel('porosity MPM (%)')
    axE.set_title(f'DEM ↔ MPM porosity (n={len(d)})', fontsize=9)
    fig.colorbar(sc, ax=axE, label='φ_SE', fraction=0.046); axE.grid(alpha=0.3); axE.set_aspect('equal')

    # ── F: standardized OLS interaction coefficients (porosity & σ_ionic) ──
    axF = fig.add_subplot(gs[1, 2])
    summary = []
    bars = {}
    for y, lab, logy in [('porosity', 'porosity', False), ('sigma_full_mScm', 'logσ_ionic', True)]:
        coef, r2, n = ols_interactions(df, y, KNOBS, logy=logy)
        if coef:
            bars[f'{lab} (R²={r2:.2f},n={n})'] = coef
            summary.append((lab, r2, n, coef))
    if bars:
        terms = list(next(iter(bars.values())).keys())
        x = np.arange(len(terms)); w = 0.8 / len(bars)
        for i, (lab, coef) in enumerate(bars.items()):
            axF.bar(x + i * w, [coef[t] for t in terms], w, label=lab)
        axF.set_xticks(x + w * (len(bars) - 1) / 2)
        axF.set_xticklabels(terms, rotation=90, fontsize=7)
        axF.axhline(0, color='k', lw=0.6)
        axF.set_ylabel('standardized β'); axF.set_title('OLS main + interaction effects', fontsize=9)
        axF.legend(fontsize=7); axF.grid(alpha=0.3, axis='y')

    fig.suptitle(f'Master interaction analysis — {len(df)} cases', fontsize=13, y=0.98)
    import os
    os.makedirs(os.path.dirname(a.out) or '.', exist_ok=True)
    fig.savefig(a.out, dpi=130, bbox_inches='tight')
    print(f'saved {a.out}')

    # text summary
    print('\n=== OLS (standardized β; |β|>0.15 = meaningful) ===')
    for lab, r2, n, coef in summary:
        print(f'\n{lab}  (R²={r2:.3f}, n={n}):')
        for t, b in sorted(coef.items(), key=lambda kv: -abs(kv[1])):
            mark = ' ★' if abs(b) > 0.15 else ''
            print(f'    {t:22s} {b:+.3f}{mark}')


if __name__ == '__main__':
    main()
