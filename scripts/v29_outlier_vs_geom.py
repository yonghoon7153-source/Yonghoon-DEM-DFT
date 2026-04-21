#!/usr/bin/env python3
"""
v29 outlier diagnostic — fit current dataset to FORM X and check whether
σ-fit outliers correlate with Physics-mode geom cap activation (%).

Core formula (FORM X v29 simplified single-term):
    σ_pred  =  C  ·  σ_grain  ·  (φ - φc)^0.75  ·  CN_SE^1.0  ·  cov^0.25  /  √τ
  fit params: C (geometric mean), φc (fixed at 0.185 by default, optional search).

Outputs to docs/figures/physics_regime/ :
  • v29_fit_per_case.csv  — case, σ_actual, σ_pred, |err|%, regime cap percentages
  • v29_outlier_geom_correlation.txt — summary stats
  • v29_parity_with_outliers.png — parity plot with outlier overlays
"""
from __future__ import annotations
import os, json, sys
from pathlib import Path
import numpy as np
import pandas as pd

SG = 3.0  # σ_grain LPSCl
WEBAPP = Path(__file__).parent.parent / 'webapp'
OUT = Path('docs/figures/physics_regime')
OUT.mkdir(parents=True, exist_ok=True)


def load_cases():
    rows = []
    for base in (WEBAPP / 'results', WEBAPP / 'archive'):
        if not base.is_dir():
            continue
        for mp in base.rglob('full_metrics.json'):
            try:
                with open(mp) as f:
                    m = json.load(f)
            except Exception:
                continue
            s_act = m.get('sigma_full_mScm')
            if not s_act or s_act < 1e-4:
                continue
            phi = m.get('phi_se')
            tau = m.get('tortuosity_mean') or m.get('tau_dij')
            cn  = m.get('se_se_cn')
            cov = m.get('coverage_AM_P_mean')
            if cov is None:
                cov = m.get('coverage_AM_S_mean')
            if cov is None:
                cov = m.get('coverage_AM_mean')
            if any(x is None for x in (phi, tau, cn, cov)):
                continue
            if tau <= 0 or phi <= 0.185 or cn <= 0:
                continue
            name_meta = WEBAPP / 'uploads' / mp.parent.name / 'meta.json'
            nm = mp.parent.name
            if name_meta.exists():
                try:
                    nm = json.load(open(name_meta)).get('name', nm)
                except Exception:
                    pass
            rows.append({
                'case_id': mp.parent.name,
                'name': nm,
                'sigma_actual': s_act,
                'phi': phi,
                'tau': tau,
                'cn': cn,
                'cov': cov / 100.0,  # fraction
                'porosity': m.get('porosity'),
            })
    # dedup by (name, round(phi,3))
    seen = {}
    for r in rows:
        k = (r['name'], round(r['phi'], 3))
        if k not in seen:
            seen[k] = r
    return list(seen.values())


def fit_form_x(df, phi_c=0.185):
    """Fit  σ = C · σ_grain · (φ-φc)^0.75 · CN · √cov / √τ   with only C free."""
    kernel = (
        (df['phi'] - phi_c).clip(lower=1e-6).pow(0.75)
        * df['cn']
        * df['cov'].pow(0.25)   # √cov → cov^0.25 to soften (matches v29 ⁴√cov)
        / df['tau'].pow(0.5)
    )
    # geometric-mean C in log space (robust to outliers)
    ln_c = np.mean(np.log(df['sigma_actual']) - np.log(SG * kernel))
    C = float(np.exp(ln_c))
    pred = C * SG * kernel
    return C, pred


def r2_log(actual, predicted):
    la, lp = np.log(actual), np.log(predicted)
    return 1 - np.sum((la - lp) ** 2) / np.sum((la - np.mean(la)) ** 2)


def main():
    rows = load_cases()
    print(f"Loaded {len(rows)} cases with valid σ/φ/τ/CN/cov")
    df = pd.DataFrame(rows)

    C, pred = fit_form_x(df)
    df['sigma_predicted'] = pred
    df['err_pct'] = 100 * (df['sigma_predicted'] - df['sigma_actual']) / df['sigma_actual']
    df['abs_err_pct'] = df['err_pct'].abs()
    r2 = r2_log(df['sigma_actual'].values, df['sigma_predicted'].values)

    print(f"\nFORM X fit (C only, φc=0.185 fixed):")
    print(f"  C = {C:.5f}")
    print(f"  R² (log-space) = {r2:.4f}")
    print(f"  ±20% band     : {(df['abs_err_pct'] <= 20).sum()}/{len(df)}")
    print(f"  |err| median  : {df['abs_err_pct'].median():.1f}%")

    # Merge with geom cap CSV from physics_regime_histogram --all
    reg_csv = OUT / 'dataset_summary.csv'
    if reg_csv.exists():
        reg = pd.read_csv(reg_csv)
        m = df.merge(reg, left_on='case_id', right_on='case_id', suffixes=('', '_reg'))
        print(f"\nMerged with regime summary: {len(m)}/{len(df)} cases matched")
    else:
        print(f"\n⚠ {reg_csv} not found — run scripts/physics_regime_histogram.py --all first")
        m = df.copy()
        m['geom'] = np.nan
        m['p50_dr'] = np.nan
        m['liggghts_lb'] = np.nan
        m['tabor'] = np.nan

    # Save per-case CSV
    cols = ['case_id', 'name', 'sigma_actual', 'sigma_predicted', 'err_pct', 'abs_err_pct',
            'phi', 'tau', 'cn', 'cov', 'porosity', 'p50_dr', 'tabor', 'geom', 'liggghts_lb']
    cols = [c for c in cols if c in m.columns]
    m_sorted = m.sort_values('abs_err_pct', ascending=False)
    csv_out = OUT / 'v29_fit_per_case.csv'
    m_sorted.to_csv(csv_out, index=False)
    print(f"\n→ {csv_out}")

    # Outlier vs geom% correlation
    outliers = m[m['abs_err_pct'] > 20]
    inliers  = m[m['abs_err_pct'] <= 20]
    print(f"\n=== Outlier analysis (|err| > 20%) ===")
    print(f"  Outliers: {len(outliers)}")
    print(f"  Inliers : {len(inliers)}")

    if 'geom' in m.columns and m['geom'].notna().any():
        # Pearson correlation between |err| and geom%
        mask = m['geom'].notna()
        corr = np.corrcoef(m.loc[mask, 'abs_err_pct'], m.loc[mask, 'geom'])[0, 1]
        print(f"\n  Pearson corr(|err|, geom%) = {corr:+.3f}")

        if len(outliers) > 0:
            print(f"\n  Outlier geom% distribution:")
            print(f"    median : {outliers['geom'].median():.2f}%")
            print(f"    mean   : {outliers['geom'].mean():.2f}%")
            print(f"    max    : {outliers['geom'].max():.2f}%")
            print(f"  Inlier geom% for reference:")
            print(f"    median : {inliers['geom'].median():.2f}%")
            print(f"    mean   : {inliers['geom'].mean():.2f}%")

        # Top 10 highest geom%
        print(f"\n=== Top 10 highest geom% ===")
        top_geom = m.sort_values('geom', ascending=False).head(10)
        for _, r in top_geom.iterrows():
            flag = ' ⚠OUTLIER' if r.get('abs_err_pct', 0) > 20 else ''
            print(f"  {r['name']:32s}  geom={r['geom']:5.1f}%  |err|={r['abs_err_pct']:5.1f}%{flag}")

    # Plot parity + outlier overlay
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(figsize=(7, 6.5))
        if 'geom' in m.columns and m['geom'].notna().any():
            sc = ax.scatter(m['sigma_actual'], m['sigma_predicted'],
                            c=m['geom'], s=50, cmap='plasma', edgecolor='k',
                            linewidth=0.3, vmin=0, vmax=20)
            plt.colorbar(sc, ax=ax, label='geom cap %')
        else:
            ax.scatter(m['sigma_actual'], m['sigma_predicted'], s=50, edgecolor='k',
                       linewidth=0.3, alpha=0.8)
        # 1:1 line and ±20%
        lo, hi = m['sigma_actual'].min() * 0.5, m['sigma_actual'].max() * 2
        ax.plot([lo, hi], [lo, hi], 'k--', lw=1, label='1:1')
        ax.fill_between([lo, hi], [lo*0.8, hi*0.8], [lo*1.2, hi*1.2],
                         alpha=0.1, color='g', label='±20%')
        ax.set_xscale('log'); ax.set_yscale('log')
        ax.set_xlabel('σ_actual (mS/cm) — network solver')
        ax.set_ylabel('σ_predicted (mS/cm) — FORM X v29')
        ax.set_title(f'v29 parity — R²={r2:.3f}, ±20% {(df["abs_err_pct"] <= 20).sum()}/{len(df)}\n'
                     'colored by physics-mode geom cap %')
        ax.legend(loc='lower right', fontsize=9)
        ax.grid(alpha=0.25, which='both')
        # Annotate top outliers
        for _, r in m.nlargest(5, 'abs_err_pct').iterrows():
            ax.annotate(r['name'][:15], (r['sigma_actual'], r['sigma_predicted']),
                        fontsize=7, alpha=0.8, xytext=(5, 5), textcoords='offset points')
        plt.tight_layout()
        png = OUT / 'v29_parity_with_outliers.png'
        fig.savefig(png, dpi=150)
        plt.close()
        print(f"\n→ {png}")
    except ImportError:
        print("\n(matplotlib not available — skipped parity plot)")


if __name__ == '__main__':
    main()
