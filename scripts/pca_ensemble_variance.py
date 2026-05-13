#!/usr/bin/env python3
"""Variance decomposition + PCA on the 82-case DEM ensemble.

For every case under webapp/archive/ that has a full_metrics.json we
extract a small feature/target table:

  Features (microstructure design knobs):
    r_AM_P_um, r_AM_S_um, r_SE_um, p_vol, s_vol, porosity_pct,
    am_wt, se_wt, n_AM_P, n_AM_S, n_SE, thickness_um (when present)

  Targets (Stage-E pipeline outputs):
    sigma_full_mScm                 ionic baseline
    sigma_full_mScm_stage_e         ionic, grain-corrected
    electronic_sigma_full_mScm
    electronic_sigma_full_mScm_stage_e
    thermal_sigma_full_mScm
    thermal_sigma_full_mScm_stage_e
    electronic_sigma_loss_pct_stage_e
    thermal_sigma_loss_pct_stage_e
    fracture_index, fracture_index_force

For each target we report:
  (a) Pearson correlation against every feature (signed effect size).
  (b) Univariate variance explained R² = corr² (single-feature fit).
  (c) Multivariate R² of a linear least-squares fit on standardised
      features (`lin_R²_all`).
  (d) Principal-component analysis of the standardised feature matrix
      and projection of each target onto the components, so the user
      can read "PC1 explains X% of the design-knob variance and Y% of
      the σ_e_stage_e variance".

The point isn't to fit a new model -- it's to separate "porosity
effect" from "P:S effect" cleanly enough that the reviewer can see
which design knob actually drives the σ_e loss in our 82-case ensemble.

Outputs:
  docs/db/pca_variance_decomposition.csv     all correlations + R²
  docs/db/pca_components.csv                 PC loadings + explained var
  docs/figures/pca_biplot.png                PC1-vs-PC2 scatter, coloured
                                              by σ_e_loss_pct_stage_e

Usage:
  python3 scripts/pca_ensemble_variance.py
"""
from __future__ import annotations
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT    = Path(__file__).resolve().parent.parent
WEBAPP  = ROOT / 'webapp'
DOCSDB  = ROOT / 'docs' / 'db'
FIGDIR  = ROOT / 'docs' / 'figures'

FEATURES = [
    'r_AM_P_um', 'r_AM_S_um', 'r_SE_um',
    'p_vol', 's_vol', 'porosity_pct',
    'am_wt', 'se_wt',
    'n_AM_P', 'n_AM_S', 'n_SE',
    'thickness_um',
]
TARGETS = [
    'sigma_full_mScm', 'sigma_full_mScm_stage_e',
    'electronic_sigma_full_mScm', 'electronic_sigma_full_mScm_stage_e',
    'thermal_sigma_full_mScm', 'thermal_sigma_full_mScm_stage_e',
    'electronic_sigma_loss_pct_stage_e', 'thermal_sigma_loss_pct_stage_e',
    'fracture_index', 'fracture_index_force',
]


def discover_cases() -> list[Path]:
    """Walk webapp/archive/ and webapp/results/ for case dirs that
    have both atoms.csv and full_metrics.json (mirrors discover logic
    used by run_network_full_corrections.py)."""
    seen, out = set(), []
    for base in ('archive', 'results'):
        root = WEBAPP / base
        if not root.exists():
            continue
        for atoms_p in root.rglob('atoms.csv'):
            d = atoms_p.parent
            if (d / 'full_metrics.json').exists() and d not in seen:
                seen.add(d)
                out.append(d)
    return sorted(out)


def _read_porosity_row(case_id: str) -> dict:
    """Pick up the matching row from all_dem_porosity.csv if it
    exists, so we have campaign / wt% / vol / r_* in one place."""
    csv_p = ROOT / 'all_dem_porosity.csv'
    if not csv_p.exists():
        return {}
    df = pd.read_csv(csv_p)
    sub = df[df['case_id'] == case_id]
    if sub.empty:
        return {}
    return sub.iloc[0].to_dict()


def collect_table() -> pd.DataFrame:
    rows = []
    for d in discover_cases():
        try:
            fm = json.loads((d / 'full_metrics.json').read_text())
        except Exception:
            continue
        rec = {'case_id': d.name}
        # Microstructure features from porosity table
        rec.update(_read_porosity_row(d.name))
        # Targets + thickness fallback from full_metrics.json
        for k in TARGETS + ['thickness_um']:
            if k in fm and fm[k] is not None:
                rec.setdefault(k, fm[k])
        rows.append(rec)
    return pd.DataFrame(rows)


def _pca(X: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Return (scores, loadings, explained_var_ratio) for column-
    standardised X. Uses SVD so it's stable when n_samples < n_features
    is not the case (we have 82 > 12)."""
    mu = X.mean(axis=0)
    sd = X.std(axis=0, ddof=0)
    sd[sd == 0] = 1.0
    Z = (X - mu) / sd
    U, S, VT = np.linalg.svd(Z, full_matrices=False)
    scores   = U * S
    loadings = VT.T
    var      = (S ** 2) / max(1, Z.shape[0] - 1)
    return scores, loadings, var / var.sum()


def main() -> None:
    df = collect_table()
    if df.empty:
        print('No case data found — nothing to decompose.', flush=True)
        sys.exit(1)
    print(f'Loaded {len(df)} cases.', flush=True)
    DOCSDB.mkdir(parents=True, exist_ok=True)
    FIGDIR.mkdir(parents=True, exist_ok=True)

    # ─ Pearson correlation table ────────────────────────────────
    feat = [c for c in FEATURES if c in df.columns]
    tgt  = [c for c in TARGETS  if c in df.columns]
    if not feat or not tgt:
        print('No usable feature/target columns. Available columns:',
              list(df.columns), flush=True)
        sys.exit(1)

    decomposition = []
    for t in tgt:
        for f in feat:
            sub = df[[f, t]].dropna()
            if len(sub) < 5:
                continue
            r = sub[f].corr(sub[t])
            if not np.isfinite(r):
                continue
            decomposition.append({
                'target':      t,
                'feature':     f,
                'pearson_r':   round(float(r), 4),
                'univariate_R2': round(float(r * r), 4),
                'n_cases':     int(len(sub)),
            })
    dec_df = pd.DataFrame(decomposition).sort_values(
        ['target', 'univariate_R2'], ascending=[True, False])

    # Multivariate R² per target (linear least squares on standardised feat)
    multi_rows = []
    for t in tgt:
        sub = df[feat + [t]].dropna()
        if len(sub) < len(feat) + 2:
            continue
        X = sub[feat].to_numpy(dtype=float)
        y = sub[t].to_numpy(dtype=float)
        mu_x = X.mean(0); sd_x = X.std(0); sd_x[sd_x == 0] = 1
        mu_y = y.mean();  sd_y = y.std() or 1
        Xs = (X - mu_x) / sd_x
        ys = (y - mu_y) / sd_y
        coef, *_ = np.linalg.lstsq(Xs, ys, rcond=None)
        yhat = Xs @ coef
        ss_res = float(((ys - yhat) ** 2).sum())
        ss_tot = float((ys ** 2).sum())
        r2 = 1 - ss_res / ss_tot if ss_tot > 0 else 0.0
        multi_rows.append({
            'target': t, 'lin_R2_all_features': round(r2, 4),
            'n_cases': int(len(sub)),
        })
    multi_df = pd.DataFrame(multi_rows)

    # ─ PCA on the standardised feature matrix ───────────────────
    sub_feat = df[feat].dropna()
    Xpca = sub_feat.to_numpy(dtype=float)
    scores, loadings, evr = _pca(Xpca)
    pc_cols = [f'PC{i+1}' for i in range(loadings.shape[1])]
    load_df = pd.DataFrame(loadings, index=feat, columns=pc_cols)
    load_df.loc['explained_var_ratio'] = evr

    # Save outputs
    dec_path  = DOCSDB / 'pca_variance_decomposition.csv'
    pc_path   = DOCSDB / 'pca_components.csv'
    multi_path = DOCSDB / 'pca_multivariate_R2.csv'
    dec_df.to_csv(dec_path, index=False)
    load_df.to_csv(pc_path)
    multi_df.to_csv(multi_path, index=False)
    print(f'  ✓ {dec_path}'); print(f'  ✓ {pc_path}'); print(f'  ✓ {multi_path}')

    # ─ PC1 vs PC2 biplot, coloured by σ_e_loss_pct_stage_e ──────
    if 'electronic_sigma_loss_pct_stage_e' in df.columns:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        joined = df.loc[sub_feat.index].reset_index(drop=True)
        loss = joined['electronic_sigma_loss_pct_stage_e'].astype(float)
        fig, ax = plt.subplots(figsize=(7.5, 6))
        sc = ax.scatter(scores[:, 0], scores[:, 1], c=loss,
                         cmap='coolwarm', s=42, edgecolor='k',
                         linewidth=0.4)
        ax.set_xlabel(f'PC1 ({100*evr[0]:.1f}% of design-knob variance)')
        ax.set_ylabel(f'PC2 ({100*evr[1]:.1f}% of design-knob variance)')
        ax.set_title('82-case ensemble — PCA biplot,\n'
                      'colour = electronic σ_e Stage-E loss (%)')
        plt.colorbar(sc, ax=ax, label='σ_e_loss_pct_stage_e')
        # Loadings as arrows
        scale_arrow = max(np.abs(scores[:, :2]).max(), 1.0) * 0.6
        for i, f in enumerate(feat):
            ax.arrow(0, 0,
                      loadings[i, 0] * scale_arrow,
                      loadings[i, 1] * scale_arrow,
                      head_width=scale_arrow*0.02,
                      color='black', alpha=0.65, length_includes_head=True)
            ax.text(loadings[i, 0] * scale_arrow * 1.10,
                     loadings[i, 1] * scale_arrow * 1.10,
                     f, fontsize=8, ha='center',
                     color='#444')
        ax.grid(alpha=0.3)
        plt.tight_layout()
        out = FIGDIR / 'pca_biplot.png'
        fig.savefig(out, dpi=150, bbox_inches='tight')
        plt.close(fig)
        print(f'  ✓ {out}')

    # Console summary
    print('\n── Top 3 features by |Pearson r| for each Stage-E target ──')
    for t in tgt:
        s = dec_df[dec_df['target'] == t].head(3)
        if s.empty: continue
        print(f'  {t}')
        for _, row in s.iterrows():
            print(f'    {row["feature"]:18s} r = {row["pearson_r"]:+.3f}  '
                  f'(R² = {row["univariate_R2"]:.3f})')


if __name__ == '__main__':
    main()
