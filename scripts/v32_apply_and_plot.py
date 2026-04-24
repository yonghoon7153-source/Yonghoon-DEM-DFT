#!/usr/bin/env python3
"""
Apply v32 correction on top of v29 FORM X and plot parity comparison.

σ_v32 = σ_v29 × exp(
    γ1 · LIGG_LB_PCT_normed
  + γ2 · THIN_X_GEOM
  + γ3 · (p50_δR − 0.20)
  + γ4 · PSD_RATIO
)

γ values fit from today's exhaustive run (4-term winner):
  γ1 = -0.750  (LIGG_LB_PCT)
  γ2 = +1.619  (THIN_X_GEOM)
  γ3 = -1.992  (P50_DR_DEV)
  γ4 = +0.348  (PSD_RATIO)

Outputs:
  docs/figures/physics_regime/v32_parity.png         — parity plot
  docs/figures/physics_regime/v32_vs_v29_compare.png — side-by-side
  docs/figures/physics_regime/v32_per_case.csv       — σ_act/v29/v32

Usage:
  python3 scripts/v32_apply_and_plot.py
  python3 scripts/v32_apply_and_plot.py --refit  # re-fit γ jointly
"""
from __future__ import annotations
import os, json, sys, argparse
from pathlib import Path
import numpy as np
import pandas as pd

SCRIPTS_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPTS_DIR))
from v32_exhaustive_refit import load_cases, build_features, v29_predict_vec  # noqa: E402
from generate_comparison_plots import _formx_v29_params  # noqa: E402

OUT = Path('docs/figures/physics_regime')
OUT.mkdir(parents=True, exist_ok=True)


# ---------- v32 4-term correction (today's fit) ----------
V32_GAMMAS_FIXED = {
    'LIGG_LB_PCT':  -0.750,
    'THIN_X_GEOM':  +1.619,
    'P50_DR_DEV':   -1.992,
    'PSD_RATIO':    +0.348,
}


def apply_v32(base_pred, features, gammas):
    correction = np.zeros(len(base_pred))
    for fname, g in gammas.items():
        correction = correction + g * features[fname]
    return base_pred * np.exp(correction)


def refit_gammas(df, base_pred, feature_names, features):
    """OLS refit of γ coefficients on log residual."""
    X = np.column_stack([features[f] for f in feature_names])
    log_actual = np.log(df['sigma_actual'].values)
    log_base = np.log(base_pred)
    residual = log_actual - log_base
    gammas, *_ = np.linalg.lstsq(X, residual, rcond=None)
    return dict(zip(feature_names, gammas))


def r2_log(actual, predicted):
    la, lp = np.log(actual), np.log(predicted)
    return 1 - np.sum((la - lp) ** 2) / np.sum((la - np.mean(la)) ** 2)


def plot_parity(ax, actual, predicted, colors, label_text, title):
    # ±20% band
    lo, hi = actual.min() * 0.5, actual.max() * 2
    ax.fill_between([lo, hi], [lo*0.8, hi*0.8], [lo*1.2, hi*1.2],
                     alpha=0.12, color='g', label='±20% band')
    ax.plot([lo, hi], [lo, hi], 'k--', lw=1, label='1:1')
    ax.scatter(actual, predicted, s=48, c=colors, cmap='plasma',
               edgecolor='k', linewidth=0.4, vmin=0, vmax=20)
    ax.set_xscale('log'); ax.set_yscale('log')
    ax.set_xlabel('σ_actual (mS/cm) — network solver')
    ax.set_ylabel('σ_predicted (mS/cm)')
    ax.grid(alpha=0.25, which='both')
    ax.legend(loc='lower right', fontsize=8)
    ax.text(0.03, 0.97, label_text, transform=ax.transAxes,
            fontsize=9, va='top', ha='left',
            bbox=dict(boxstyle='round,pad=0.4', facecolor='white',
                       edgecolor='gray', alpha=0.9))
    ax.set_title(title, fontsize=10)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--refit', action='store_true',
                    help='Re-fit γ coefficients jointly with current data')
    args = ap.parse_args()

    rows = load_cases()
    df = pd.DataFrame(rows)
    n = len(df)
    print(f"Loaded {n} cases")

    # v29 predictions
    params = _formx_v29_params()
    v29_pred = v29_predict_vec(df, params)

    # Features for v32 correction
    features = build_features(df)

    # Fit or use fixed γ
    if args.refit:
        feats = list(V32_GAMMAS_FIXED.keys())
        gammas = refit_gammas(df, v29_pred, feats, features)
        print(f"\nRefit γ coefficients:")
        for f, g in gammas.items():
            print(f"  γ({f:13s}) = {g:+.4f}")
    else:
        gammas = V32_GAMMAS_FIXED
        print(f"\nUsing FIXED γ from today's exhaustive run:")
        for f, g in gammas.items():
            print(f"  γ({f:13s}) = {g:+.4f}")

    v32_pred = apply_v32(v29_pred, features, gammas)

    actual = df['sigma_actual'].values
    r2_v29 = r2_log(actual, v29_pred)
    r2_v32 = r2_log(actual, v32_pred)

    err_v29 = np.abs(v29_pred - actual) / actual * 100
    err_v32 = np.abs(v32_pred - actual) / actual * 100
    w20_v29 = int(np.sum(err_v29 < 20))
    w20_v32 = int(np.sum(err_v32 < 20))

    print(f"\n=== Fit Quality ===")
    print(f"                v29 (defaults)   v32 (4-term)")
    print(f"  R² (log)    = {r2_v29:.4f}           {r2_v32:.4f}")
    print(f"  ±20% band   = {w20_v29}/{n}              {w20_v32}/{n}")
    print(f"  |err| median= {np.median(err_v29):5.1f}%             {np.median(err_v32):5.1f}%")
    print(f"  |err| max   = {np.max(err_v29):5.1f}%            {np.max(err_v32):5.1f}%")

    # Dump per-case CSV
    out_df = df[['case_id', 'name', 'sigma_actual', 'phi', 'tau',
                  'thick', 'porosity', 'geom_pct', 'liggghts_lb_pct', 'p50_dr']].copy()
    out_df['sigma_pred_v29'] = v29_pred
    out_df['sigma_pred_v32'] = v32_pred
    out_df['err_pct_v29'] = 100 * (v29_pred - actual) / actual
    out_df['err_pct_v32'] = 100 * (v32_pred - actual) / actual
    csv_out = OUT / 'v32_per_case.csv'
    out_df.sort_values('err_pct_v32', key=lambda x: x.abs(), ascending=False).to_csv(csv_out, index=False)
    print(f"\n→ {csv_out}")

    # Plot
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt

        # ── Single parity (v32 only) ──
        fig, ax = plt.subplots(figsize=(7.5, 6.5))
        title1 = (
            r"FORM X v32 = v29_FINAL $\times$ exp($-0.75 \cdot$LIGG$\_$LB $+1.62 \cdot$w$_{\rm thin}\cdot$GEOM$ -1.99 \cdot (p_{50}\delta R-0.2) +0.35 \cdot r_{SE}/r_{AM}$)"
        )
        label1 = (f"R² = {r2_v32:.4f}  (n={n})\n"
                  f"±20% band = {w20_v32}/{n}\n"
                  f"|err| median = {np.median(err_v32):.1f}%")
        plot_parity(ax, actual, v32_pred,
                     colors=df['geom_pct'].values, label_text=label1, title=title1)
        # annotate top-5 outliers by |err_v32|
        top5_idx = err_v32.argsort()[-5:][::-1]
        for i in top5_idx:
            ax.annotate(df.iloc[i]['name'][:15],
                         (actual[i], v32_pred[i]),
                         fontsize=7, alpha=0.8,
                         xytext=(5, 5), textcoords='offset points')
        # colorbar
        sc_dummy = ax.scatter([], [], c=[], cmap='plasma', vmin=0, vmax=20)
        plt.colorbar(sc_dummy, ax=ax, label='physics-mode geom cap %')
        plt.tight_layout()
        p1 = OUT / 'v32_parity.png'
        fig.savefig(p1, dpi=150)
        plt.close()
        print(f"→ {p1}")

        # ── Side-by-side v29 vs v32 ──
        fig, axes = plt.subplots(1, 2, figsize=(14, 6), sharex=True, sharey=True)
        plot_parity(axes[0], actual, v29_pred,
                     colors=df['geom_pct'].values,
                     label_text=f"R² = {r2_v29:.4f}\n±20% = {w20_v29}/{n}\n|err| med = {np.median(err_v29):.1f}%",
                     title="v29 FORM X FINAL (defaults)")
        plot_parity(axes[1], actual, v32_pred,
                     colors=df['geom_pct'].values,
                     label_text=f"R² = {r2_v32:.4f}\n±20% = {w20_v32}/{n}\n|err| med = {np.median(err_v32):.1f}%",
                     title="v32 = v29 × exp(4-term correction)")
        plt.suptitle(f'Scaling-law improvement v29 → v32 (n={n} cases)', fontsize=11)
        plt.tight_layout()
        p2 = OUT / 'v32_vs_v29_compare.png'
        fig.savefig(p2, dpi=150)
        plt.close()
        print(f"→ {p2}")

    except ImportError as e:
        print(f"matplotlib unavailable: {e}")


if __name__ == '__main__':
    main()
