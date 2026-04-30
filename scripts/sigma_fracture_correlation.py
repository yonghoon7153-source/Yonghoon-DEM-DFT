#!/usr/bin/env python3
"""Quick analysis: correlation of σ_electronic and σ_thermal with the
Auerbach-Lawn fracture index across the 78-case ensemble.

Purpose
───────
Section 4 of the paper draft argues that σ_ionic is robust to AM-AM
fracture interpretation because the ionic network solver sees only
SE-SE edges. That argument does NOT extend to σ_electronic (AM-AM
network) or σ_thermal (all contacts including AM-AM). This script
quantifies how strongly the two non-ionic channels move with the
fracture index, providing the empirical basis for either:

  (a) extending the brittle-caveat draft with a Section 6 on σ_e and
      σ_thermal sensitivity, or
  (b) noting in Section 4 that the companion analysis must address
      these channels separately.

Output
──────
Pearson + Spearman correlations between each σ channel and
fracture_index (δ-based) and fracture_index_force (force-based) across
the available cases. If |r| < 0.3 the channel is largely insensitive
to AM fracture; |r| > 0.5 indicates a clear coupling.
"""
from __future__ import annotations
from pathlib import Path
import sys

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
DB_CSV = ROOT / 'docs' / 'db' / 'metrics_master.csv'


def _pearson(x, y):
    x = np.asarray(x, float); y = np.asarray(y, float)
    m = ~(np.isnan(x) | np.isnan(y))
    if m.sum() < 5: return float('nan'), 0
    x, y = x[m], y[m]
    if x.std() == 0 or y.std() == 0: return float('nan'), len(x)
    return float(np.corrcoef(x, y)[0, 1]), len(x)


def _spearman(x, y):
    x = np.asarray(x, float); y = np.asarray(y, float)
    m = ~(np.isnan(x) | np.isnan(y))
    if m.sum() < 5: return float('nan'), 0
    x, y = x[m], y[m]
    rx = pd.Series(x).rank().values
    ry = pd.Series(y).rank().values
    if rx.std() == 0 or ry.std() == 0: return float('nan'), len(x)
    return float(np.corrcoef(rx, ry)[0, 1]), len(x)


def main() -> None:
    if not DB_CSV.exists():
        sys.exit(f'metrics_master.csv not found at {DB_CSV}')
    df = pd.read_csv(DB_CSV)
    print(f'Loaded {len(df)} cases.\n', flush=True)

    sigma_cols = [
        ('σ_ionic',       'sigma_full_mScm'),
        ('σ_electronic',  'electronic_sigma_full_mScm'),
        ('σ_thermal',     'thermal_sigma_full_mScm'),
    ]
    fracture_cols = [
        ('fracture_index (δ-based)',     'fracture_index'),
        ('fracture_index_force',          'fracture_index_force'),
    ]

    print('=' * 78, flush=True)
    print('Correlation of σ-channels with AM-AM fracture indices', flush=True)
    print('=' * 78, flush=True)
    print(f'  {"":24s} {"Pearson r":>12s} {"Spearman r":>12s} {"n":>6s}  Interpretation',
          flush=True)
    print('  ' + '-' * 75, flush=True)

    for s_label, s_col in sigma_cols:
        if s_col not in df.columns:
            print(f'  {s_label:24s}  (column missing)', flush=True)
            continue
        for f_label, f_col in fracture_cols:
            if f_col not in df.columns:
                continue
            # log σ for ionic / electronic to compare across orders of magnitude
            if 'σ_ionic' in s_label or 'σ_electronic' in s_label:
                y = np.log(np.maximum(df[s_col].astype(float).values, 1e-12))
            else:
                y = df[s_col].astype(float).values
            x = df[f_col].astype(float).values
            r_p, n = _pearson(x, y)
            r_s, _ = _spearman(x, y)
            absr = abs(r_p) if not np.isnan(r_p) else 0
            if   absr < 0.20: tag = 'no coupling'
            elif absr < 0.40: tag = 'weak'
            elif absr < 0.60: tag = 'moderate'
            else:             tag = 'STRONG coupling'
            head = f'{s_label} vs {f_label}'
            print(f'  {head:42s}  '
                  f'{r_p:>+8.3f}  '
                  f'{r_s:>+8.3f}    '
                  f'{n:>4d}   {tag}', flush=True)
        print()

    # Additional diagnostic: change in σ_e between cases at low vs high fracture_index
    print('\nMedian σ comparison across fracture_index quartiles:', flush=True)
    if 'fracture_index' in df.columns:
        d = df.copy()
        d['frac_q'] = pd.qcut(d['fracture_index'], q=4, labels=['Q1 (low)', 'Q2', 'Q3', 'Q4 (high)'],
                                duplicates='drop')
        print(f'  {"Quartile":<14s} {"σ_ionic":>10s} {"σ_electronic":>14s} {"σ_thermal":>12s} {"n":>4s}',
              flush=True)
        print('  ' + '-' * 60, flush=True)
        for q in d['frac_q'].dropna().unique():
            sub = d[d['frac_q'] == q]
            si = sub['sigma_full_mScm'].median() if 'sigma_full_mScm' in sub.columns else float('nan')
            se = sub['electronic_sigma_full_mScm'].median() if 'electronic_sigma_full_mScm' in sub.columns else float('nan')
            st = sub['thermal_sigma_full_mScm'].median() if 'thermal_sigma_full_mScm' in sub.columns else float('nan')
            print(f'  {str(q):<14s} {si:>10.4f} {se:>14.3f} {st:>12.3f} {len(sub):>4d}',
                  flush=True)


if __name__ == '__main__':
    main()
