#!/usr/bin/env python3
"""
v29 outlier diagnostic — uses the EXACT v29 FORM X FINAL formula from
scripts/generate_comparison_plots.py (_formx_v29_predict), fits σ_pred
per case, and correlates |residual| with Physics-mode geom cap %.

v29 FINAL (from plot title):
  σ = C_blend(τ) · C_pf(p) · G(τ,p) · C_gb(sigmoid)
      × σ_grain × √(φ−0.2) × CN^(3/2) × cov^(2/5) × f_p³

Parameters live in _formx_v29_params() (module globals written by the
group-plot pipeline). We import both.

Outputs to docs/figures/physics_regime/:
  • v29_fit_per_case.csv            per-case σ_actual, σ_pred, %err, cap columns
  • v29_parity_with_outliers.png    parity colored by geom cap %
  • stdout summary                   Pearson corr + top-10 geom% cases
"""
from __future__ import annotations
import os, json, sys
from pathlib import Path
import numpy as np
import pandas as pd

SCRIPTS_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPTS_DIR))

# Import the EXACT v29 predictor
from generate_comparison_plots import _formx_v29_predict, _formx_v29_params, _ps_fraction  # noqa: E402

WEBAPP = Path(__file__).parent.parent / 'webapp'
OUT = Path('docs/figures/physics_regime')
OUT.mkdir(parents=True, exist_ok=True)


def _get(d, key, default=None):
    v = d.get(key, default)
    return v if v is not None else default


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
            tau = m.get('tortuosity_recommended') or m.get('tortuosity_mean') or m.get('tau_dij')
            cn  = m.get('se_se_cn')
            # coverage average from any variant
            cov_vals = [v for v in (m.get('coverage_AM_P_mean'),
                                     m.get('coverage_AM_S_mean'),
                                     m.get('coverage_AM_mean')) if v and v > 0]
            cov = (sum(cov_vals) / len(cov_vals) / 100) if cov_vals else 0.20
            # f_perc from percolation fraction
            fp = m.get('percolation_pct')
            fp = (fp / 100.0) if fp else 0.5
            gb = m.get('gb_density_mean', 1e-6) or 1e-6

            # Need ps_ratio from meta.json
            name_meta = WEBAPP / 'uploads' / mp.parent.name / 'meta.json'
            nm = mp.parent.name
            ps_ratio = ""
            if name_meta.exists():
                try:
                    mj = json.load(open(name_meta))
                    nm = mj.get('name', nm)
                    ps_ratio = mj.get('ps_ratio', '')
                except Exception:
                    pass

            if any(x is None for x in (phi, tau, cn)) or tau <= 0 or phi <= 0.20 or cn <= 0:
                continue

            # _ps_fraction expects dict with 'ps_ratio' key
            p_frac = _ps_fraction({'ps_ratio': ps_ratio})

            rows.append({
                'case_id': mp.parent.name,
                'name': nm,
                'sigma_actual': s_act,
                'phi': phi,
                'tau': tau,
                'cn': cn,
                'cov': cov,
                'f_perc': max(fp, 0.01),
                'p_frac': p_frac,
                'gb_dens': gb,
                'porosity': m.get('porosity'),
                'ps_ratio': ps_ratio,
            })
    # dedup
    seen = {}
    for r in rows:
        k = (r['name'], round(r['phi'], 3))
        if k not in seen:
            seen[k] = r
    return list(seen.values())


def r2_log(actual, predicted):
    la, lp = np.log(actual), np.log(predicted)
    return 1 - np.sum((la - lp) ** 2) / np.sum((la - np.mean(la)) ** 2)


def main():
    rows = load_cases()
    print(f"Loaded {len(rows)} cases with valid σ/φ/τ/CN")

    # Use v29 default params — to get the FITTED params that produced the
    # user's R²=0.983 plot, the group-comparison pipeline must have written
    # _GLOBAL_IONIC_SIGMOID and _GLOBAL_PS_SIGMOID into the module. Since we
    # run this diagnostic STANDALONE, we use the hard-coded defaults in
    # _formx_v29_params(). R² here may differ slightly from the group plot
    # because the globals aren't populated — that's expected.
    params = _formx_v29_params()
    print(f"Using v29 params: TC_BL={params['TC_BL']}, K_BL={params['K_BL']}, "
          f"PC_PF={params['PC_PF']}, K_PF={params['K_PF']}")
    print(f"  B_PF={params['B_PF']:+.3f}, B_LIN={params['B_LIN']:+.3f}, "
          f"B_GB={params['B_GB']:+.3f}")

    # Predict per case using the real v29 formula
    preds = []
    for r in rows:
        p = _formx_v29_predict(
            r['phi'], r['cn'], r['tau'], r['cov'], r['f_perc'],
            r['p_frac'], r['gb_dens'], params=params)
        preds.append(p)

    df = pd.DataFrame(rows)
    df['sigma_predicted'] = preds
    df['sigma_predicted'] = df['sigma_predicted'].replace(0, np.nan).fillna(1e-6)
    df['err_pct'] = 100 * (df['sigma_predicted'] - df['sigma_actual']) / df['sigma_actual']
    df['abs_err_pct'] = df['err_pct'].abs()
    r2 = r2_log(df['sigma_actual'].values, df['sigma_predicted'].values)

    print(f"\nFORM X v29 FINAL fit (defaults):")
    print(f"  R² (log-space) = {r2:.4f}")
    print(f"  ±20% band     : {(df['abs_err_pct'] <= 20).sum()}/{len(df)}")
    print(f"  |err| median  : {df['abs_err_pct'].median():.1f}%")

    reg_csv = OUT / 'dataset_summary.csv'
    if reg_csv.exists():
        reg = pd.read_csv(reg_csv)
        m = df.merge(reg, left_on='case_id', right_on='case_id', suffixes=('', '_reg'))
        print(f"\nMerged with regime summary: {len(m)}/{len(df)} cases matched")
    else:
        print(f"\n⚠ {reg_csv} not found — run physics_regime_histogram.py --all first")
        m = df.copy()
        for c in ('geom', 'p50_dr', 'liggghts_lb', 'tabor'):
            m[c] = np.nan

    cols = ['case_id', 'name', 'ps_ratio', 'sigma_actual', 'sigma_predicted',
            'err_pct', 'abs_err_pct', 'phi', 'tau', 'cn', 'cov', 'f_perc', 'p_frac',
            'porosity', 'p50_dr', 'tabor', 'geom', 'liggghts_lb']
    cols = [c for c in cols if c in m.columns]
    m_sorted = m.sort_values('abs_err_pct', ascending=False)
    csv_out = OUT / 'v29_fit_per_case.csv'
    m_sorted.to_csv(csv_out, index=False)
    print(f"\n→ {csv_out}")

    outliers = m[m['abs_err_pct'] > 20]
    inliers  = m[m['abs_err_pct'] <= 20]
    print(f"\n=== Outlier analysis (|err| > 20%) ===")
    print(f"  Outliers: {len(outliers)}")
    print(f"  Inliers : {len(inliers)}")

    if 'geom' in m.columns and m['geom'].notna().any():
        mask = m['geom'].notna()
        corr = np.corrcoef(m.loc[mask, 'abs_err_pct'], m.loc[mask, 'geom'])[0, 1]
        print(f"\n  Pearson corr(|err|, geom%) = {corr:+.3f}")
        if len(outliers) > 0:
            print(f"\n  Outlier geom% distribution:")
            print(f"    median : {outliers['geom'].median():.2f}%")
            print(f"    mean   : {outliers['geom'].mean():.2f}%")
            print(f"    max    : {outliers['geom'].max():.2f}%")
            print(f"  Inlier reference:")
            print(f"    median : {inliers['geom'].median():.2f}%")
            print(f"    mean   : {inliers['geom'].mean():.2f}%")

        print(f"\n=== Top 10 highest geom% ===")
        for _, r in m.sort_values('geom', ascending=False).head(10).iterrows():
            flag = ' ⚠OUTLIER' if r.get('abs_err_pct', 0) > 20 else ''
            print(f"  {r['name']:32s}  geom={r['geom']:5.1f}%  |err|={r['abs_err_pct']:5.1f}%{flag}")

        print(f"\n=== All outliers (|err| > 20%) ===")
        for _, r in outliers.sort_values('abs_err_pct', ascending=False).iterrows():
            print(f"  {r['name']:32s}  |err|={r['abs_err_pct']:5.1f}%  "
                  f"geom={r.get('geom','?'):>5}%  "
                  f"σ_act={r['sigma_actual']:.4f}  σ_pred={r['sigma_predicted']:.4f}  "
                  f"ps={r['ps_ratio']}")

    # Parity plot
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(figsize=(7.5, 6.5))
        if 'geom' in m.columns and m['geom'].notna().any():
            sc = ax.scatter(m['sigma_actual'], m['sigma_predicted'],
                            c=m['geom'], s=55, cmap='plasma', edgecolor='k',
                            linewidth=0.3, vmin=0, vmax=20)
            plt.colorbar(sc, ax=ax, label='geom cap %')
        else:
            ax.scatter(m['sigma_actual'], m['sigma_predicted'], s=55, edgecolor='k',
                       linewidth=0.3, alpha=0.8)
        lo, hi = m['sigma_actual'].min() * 0.5, m['sigma_actual'].max() * 2
        ax.plot([lo, hi], [lo, hi], 'k--', lw=1, label='1:1')
        ax.fill_between([lo, hi], [lo*0.8, hi*0.8], [lo*1.2, hi*1.2],
                         alpha=0.1, color='g', label='±20%')
        ax.set_xscale('log'); ax.set_yscale('log')
        ax.set_xlabel('σ_actual (mS/cm) — network solver')
        ax.set_ylabel('σ_predicted (mS/cm) — FORM X v29 FINAL')
        ax.set_title(f'v29 FINAL parity — R²={r2:.3f}, ±20% {(df["abs_err_pct"] <= 20).sum()}/{len(df)}\n'
                     'colored by Physics-mode geom cap %')
        ax.legend(loc='lower right', fontsize=9)
        ax.grid(alpha=0.25, which='both')
        for _, r in m.nlargest(5, 'abs_err_pct').iterrows():
            ax.annotate(r['name'][:15], (r['sigma_actual'], r['sigma_predicted']),
                        fontsize=7, alpha=0.8, xytext=(5, 5), textcoords='offset points')
        plt.tight_layout()
        png = OUT / 'v29_parity_with_outliers.png'
        fig.savefig(png, dpi=150)
        plt.close()
        print(f"\n→ {png}")
    except ImportError:
        print("\n(matplotlib not available)")


if __name__ == '__main__':
    main()
