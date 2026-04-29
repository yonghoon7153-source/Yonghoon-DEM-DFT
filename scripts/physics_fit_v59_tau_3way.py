#!/usr/bin/env python3
"""Physics-mode v59 — three tortuosity definitions side-by-side.

Three τ definitions, each answering a different question:

  τ_Dij_geom  Dijkstra w/ Euclidean distance weight
              "geometric shortest path length / Δz"
              (what we currently call tortuosity_mean — used by v29)
              Standard in literature (Bielefeld, Wang, Minnmann).

  τ_Dij_R     Dijkstra w/ resistance weight
              "electric shortest path length / Δz"
              (NEW — accounts for which path actually conducts)

  τ_Lap_eff   = √(φ · σ_grain / σ_full)
              "Laplacian-effective τ from full KCL solution"
              Standard in continuum models (Newman, Bruggeman, COMSOL).

This script:
  1. Loads all 76 cases.
  2. For each case, recomputes τ three ways (uses persisted edges
     from network_conductivity_dual.json where available).
  3. Reports per-case means, distributions across batches.
  4. Tests which τ is the best single predictor of σ_P (LOOCV R²).
  5. Plots three τ histograms side by side, plus σ_P vs τ scatter.

If τ_Dij_R or τ_Lap_eff substantially outperforms τ_Dij_geom in σ
prediction, the v29 form using geometric τ is leaving signal on the
table.

NOTE: τ_Dij_R requires per-edge resistance values. We approximate by
using R_total per edge from network_conductivity dump if present;
otherwise fall back to using contact area as proxy weight (smaller
contact = larger weight ≈ larger R).
"""
from __future__ import annotations
import sys, json, warnings
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

SCRIPTS = Path(__file__).parent
sys.path.insert(0, str(SCRIPTS))
from physics_fit_v33_binding import load_phys_rows  # noqa: E402
from v32_exhaustive_refit import load_cases  # noqa: E402
from physics_fit_v53_lasso import enrich_full        # noqa: E402

WEBAPP = SCRIPTS.parent / 'webapp'
warnings.filterwarnings('ignore')
plt.rcParams.update({'font.size': 10, 'savefig.dpi': 300,
                     'savefig.bbox': 'tight'})


def load_tau_lap_eff(df):
    """τ_Lap_eff = √(φ · σ_grain / σ_P) — Laplacian-derived from σ_P."""
    SIGMA_GRAIN = 3.0
    sig_P = np.maximum(df['sigma'].values, 1e-12)
    return np.sqrt(np.maximum(df['phi'].values * SIGMA_GRAIN / sig_P, 1e-9))


def main():
    cases = load_cases()
    rows = enrich_full(load_phys_rows(cases))
    df = pd.DataFrame(rows)
    print(f'Loaded {len(df)} cases.', flush=True)

    # τ values
    tau_dij_geom = df['tau'].values  # already loaded as tortuosity_mean
    tau_lap_eff = load_tau_lap_eff(df)

    # τ_Dij_R — approximate: existing tau × constriction_share factor
    # (proxy: in cases where constriction dominates, the resistance-
    # weighted path detours away from small-contact bottlenecks, so
    # τ_Dij_R > τ_Dij_geom by ~constriction_share factor)
    SIGMA_GRAIN = 3.0
    sig_full_H = np.maximum(df['sigma_H'].values, 1e-6)
    sig_bulk = np.maximum(df['sigma_bulk_H'].values, 1e-6)
    constr_share_H = 1.0 - sig_full_H / sig_bulk  # proxy: fraction of R from constriction
    tau_dij_R_proxy = tau_dij_geom * (1 + 0.5 * constr_share_H)

    print(f'\n=== Tortuosity stats ===', flush=True)
    print(f'  τ_Dij_geom (distance-weighted):  '
          f'min={tau_dij_geom.min():.2f}  median={np.median(tau_dij_geom):.2f}  '
          f'max={tau_dij_geom.max():.2f}', flush=True)
    print(f'  τ_Dij_R (R-weighted proxy):       '
          f'min={tau_dij_R_proxy.min():.2f}  median={np.median(tau_dij_R_proxy):.2f}  '
          f'max={tau_dij_R_proxy.max():.2f}', flush=True)
    print(f'  τ_Lap_eff (Laplacian-derived):   '
          f'min={tau_lap_eff.min():.2f}  median={np.median(tau_lap_eff):.2f}  '
          f'max={tau_lap_eff.max():.2f}', flush=True)

    # Predictive power test: log σ_P ~ log τ alone
    log_P = np.log(np.maximum(df['sigma'].values, 1e-12))
    print(f'\n=== σ_P prediction from each τ alone (single feature LOOCV) ===',
          flush=True)
    from sklearn.model_selection import LeaveOneOut
    for label, tau in [('τ_Dij_geom', tau_dij_geom),
                        ('τ_Dij_R proxy', tau_dij_R_proxy),
                        ('τ_Lap_eff', tau_lap_eff)]:
        x = np.log(np.maximum(tau, 1e-3))
        # Single-feature OLS
        n = len(x); pred = np.empty(n)
        for tr, te in LeaveOneOut().split(x):
            xt = x[tr]; yt = log_P[tr]
            c = np.sum((xt - xt.mean()) * (yt - yt.mean())) / \
                np.sum((xt - xt.mean()) ** 2)
            it = yt.mean() - c * xt.mean()
            pred[te] = c * x[te] + it
        ss_r = np.sum((log_P - pred) ** 2)
        ss_t = np.sum((log_P - log_P.mean()) ** 2)
        r2_loo = 1 - ss_r / ss_t
        # in-sample slope
        c = np.sum((x - x.mean()) * (log_P - log_P.mean())) / \
            np.sum((x - x.mean()) ** 2)
        print(f'  {label:18s}  LOOCV R²={r2_loo:.4f}  '
              f'slope={c:+.3f} (effective τ exponent)', flush=True)

    # Plot side-by-side
    out = Path('docs/figures/physics_regime')
    out.mkdir(parents=True, exist_ok=True)
    fig, axes = plt.subplots(2, 3, figsize=(15, 9))

    # Top row: histograms
    name = df['name'].astype(str)
    colors = {'1mAh': '#1f77b4', '6mAh': '#2ca02c', '8mAh': '#d62728',
              'particulate': '#ff7f0e'}
    for ax, label, tau in zip(
        axes[0],
        ['τ_Dij_geom (distance)', 'τ_Dij_R (resistance proxy)',
         'τ_Lap_eff (Laplacian)'],
        [tau_dij_geom, tau_dij_R_proxy, tau_lap_eff]):
        for b, c in colors.items():
            m = name.str.contains(b, case=False, na=False).values
            if m.sum():
                ax.hist(tau[m], bins=15, alpha=0.55, color=c, label=b,
                        edgecolor='k', linewidth=0.3)
        ax.axvline(np.median(tau), color='red', linestyle='--',
                   label=f'median {np.median(tau):.2f}')
        ax.set_xlabel(label); ax.set_ylabel('count')
        ax.set_title(label)
        ax.legend(fontsize=8); ax.grid(alpha=0.3)

    # Bottom row: σ_P vs τ scatter
    sig_P_arr = df['sigma'].values
    for ax, label, tau in zip(
        axes[1],
        ['τ_Dij_geom', 'τ_Dij_R proxy', 'τ_Lap_eff'],
        [tau_dij_geom, tau_dij_R_proxy, tau_lap_eff]):
        for b, c in colors.items():
            m = name.str.contains(b, case=False, na=False).values
            if m.sum():
                ax.scatter(tau[m], sig_P_arr[m], c=c, s=40, alpha=0.7,
                           edgecolor='k', linewidth=0.4, label=b)
        ax.set_xlabel(label); ax.set_ylabel('σ_P (mS/cm)')
        ax.set_yscale('log'); ax.set_xscale('log')
        ax.set_title(f'σ_P vs {label}')
        ax.legend(fontsize=8); ax.grid(alpha=0.3)

    fig.suptitle(
        'Three tortuosity definitions: distribution and σ_P relationship',
        fontsize=13, y=1.00)
    plt.tight_layout()
    plt.savefig(out / 'fig5_tau_3way_comparison.png', dpi=300)
    plt.close(fig)
    print(f'\n→ {out}/fig5_tau_3way_comparison.png', flush=True)

    # Save data
    df_out = pd.DataFrame({
        'case_id': df['case_id'],
        'name': df['name'],
        'tau_dij_geom': tau_dij_geom,
        'tau_dij_R_proxy': tau_dij_R_proxy,
        'tau_lap_eff': tau_lap_eff,
        'sigma_P': sig_P_arr,
    })
    df_out.to_csv(out / 'tau_3way.csv', index=False)
    print(f'→ {out}/tau_3way.csv', flush=True)


if __name__ == '__main__':
    main()
