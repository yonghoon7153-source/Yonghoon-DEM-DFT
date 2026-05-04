#!/usr/bin/env python3
"""Diagnose the 22 cases that section7_fracture_aware_analysis.py filters
out as numerical anomalies, plus the systematic-negative-loss check.

Why this exists
───────────────
section7's _filter_anomalies() drops cases on three criteria:

  - sigma_e_full        out of [0, 100) mS/cm
  - sigma_e_fracture_aware  out of [0, 100)
  - sigma_e_loss_pct    out of [-5, 100]

After the input_params.json fix (commit a3d9a34) most σ values became
correct, but 22 of 80 cases still get filtered. We need to know:

  (1) Which 22 cases? (case_id list)
  (2) Why each was filtered? (which criterion violated)
  (3) Are they real numerical instability, or do they expose another bug?
  (4) For the surviving 58, is the negative-loss tail (≈ -1%) systemic
      or random noise?

Output
──────
Console table of the 22 filtered cases with their failing values, plus
distribution stats on near-zero and negative loss% across all 80 cases.

Usage:
  python3 scripts/diag_section7_anomalies.py
  python3 scripts/diag_section7_anomalies.py --show-csv  # write diag CSV
"""
from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT     = Path(__file__).resolve().parent.parent
WEBAPP   = ROOT / 'webapp'
DB_DIR   = ROOT / 'docs' / 'db'


def discover_case_dirs() -> list[Path]:
    out = []
    for base in ('results', 'archive'):
        root = WEBAPP / base
        if not root.exists():
            continue
        for d in sorted(root.iterdir()):
            if d.is_dir() and (d / 'full_metrics.json').exists():
                out.append(d)
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--show-csv', action='store_true',
                    help='Write per-case diagnostic CSV to docs/db/')
    args = ap.parse_args()

    rows = []
    for d in discover_case_dirs():
        try:
            fm = json.load(open(d / 'full_metrics.json'))
        except Exception:
            continue
        rows.append({
            'case_id':    d.name,
            'σ_e_full':   fm.get('electronic_sigma_full_mScm'),
            'σ_e_fa':     fm.get('electronic_sigma_full_mScm_fracture_aware'),
            'σ_e_sw':     fm.get('electronic_sigma_full_mScm_stagewise'),
            'σ_e_E':      fm.get('electronic_sigma_full_mScm_stage_e'),
            'loss_C':     fm.get('electronic_sigma_loss_pct'),
            'loss_D':     fm.get('electronic_sigma_loss_pct_stagewise'),
            'loss_E':     fm.get('electronic_sigma_loss_pct_stage_e'),
            'σ_ionic':    fm.get('sigma_full_mScm'),
            'σ_ionic_E':  fm.get('sigma_full_mScm_stage_e'),
            'percolation': fm.get('percolation_pct') or fm.get('top_reachable_pct'),
            'n_AM_AM':    fm.get('n_total_AM_AM') or fm.get('n_am_am_contacts_total'),
        })
    df = pd.DataFrame(rows)
    print(f'Loaded {len(df)} cases.\n')

    # Apply same filter as section7
    valid_full = df['σ_e_full'].fillna(-1).between(0, 100, inclusive='left')
    valid_fa   = df['σ_e_fa'].fillna(-1).between(0, 100, inclusive='left')
    valid_loss = df['loss_C'].fillna(0).between(-5, 100)
    survive = valid_full & valid_fa & valid_loss
    n_drop = (~survive).sum()
    print(f'Dropped {n_drop} cases by section7 anomaly filter.\n')

    drop_df = df[~survive].copy()
    drop_df['fail_full'] = ~valid_full[~survive]
    drop_df['fail_fa']   = ~valid_fa[~survive]
    drop_df['fail_loss'] = ~valid_loss[~survive]

    print('=== 22 dropped cases ===')
    print(f'{"case_id":36s} {"σ_e_full":>10s} {"σ_e_fa":>10s} '
          f'{"loss_C":>8s} {"perc%":>7s} {"n_AM":>6s} reason')
    print('-' * 100)
    for _, r in drop_df.iterrows():
        reasons = []
        if r['fail_full']: reasons.append(f'σ_e_full={r["σ_e_full"]}')
        if r['fail_fa']:   reasons.append(f'σ_e_fa={r["σ_e_fa"]}')
        if r['fail_loss']: reasons.append(f'loss_C={r["loss_C"]}')
        f = lambda v: f'{v:.2f}' if v is not None and not pd.isna(v) else '-'
        n_am_v = r.get('n_AM_AM') if 'n_AM_AM' in r.index else None
        n_am_disp = (str(int(n_am_v)) if n_am_v and not pd.isna(n_am_v) else '-')
        print(f'{r["case_id"]:36s} {f(r["σ_e_full"]):>10s} {f(r["σ_e_fa"]):>10s} '
              f'{f(r["loss_C"]):>8s} {f(r["percolation"]):>7s} '
              f'{n_am_disp:>6s} {"; ".join(reasons)}')

    # Categorize drop reasons
    print('\n=== Drop reason summary ===')
    print(f'  fail σ_e_full out of [0,100):  {drop_df["fail_full"].sum()}')
    print(f'  fail σ_e_fa   out of [0,100):  {drop_df["fail_fa"].sum()}')
    print(f'  fail loss_C   out of [-5,100]: {drop_df["fail_loss"].sum()}')

    # Cross-check: do dropped cases have low percolation? (= disconnected graph)
    perc_low = drop_df['percolation'].fillna(0) < 10
    print(f'\n  of dropped: {perc_low.sum()} have percolation < 10 % '
          '(network mostly disconnected → genuine numerical issue)')

    # Negative loss check across full 80
    print('\n=== Negative loss% systematic check ===')
    for col in ['loss_C', 'loss_D', 'loss_E']:
        vals = df[col].dropna()
        neg = vals[vals < 0]
        tiny_neg = neg[neg > -1.0]
        if len(vals) == 0:
            continue
        print(f'  {col}: n={len(vals):3d}  '
              f'neg={len(neg):3d} ({len(neg)/len(vals)*100:5.1f}%)  '
              f'tiny-neg(>-1%)={len(tiny_neg):3d}  '
              f'min={vals.min():7.2f}%  '
              f'mean(neg)={(neg.mean() if len(neg) else 0):7.3f}%')

    # Are negative-loss cases biased toward any r_SE band or %severe?
    neg_e = df[df['loss_E'].fillna(0) < -0.5][['case_id', 'σ_e_full',
                                                'σ_e_E', 'loss_E', 'n_AM_AM']]
    if len(neg_e):
        print('\n=== Stage E cases with loss < -0.5% (sigma INCREASED after correction) ===')
        print(neg_e.to_string(index=False))

    if args.show_csv:
        DB_DIR.mkdir(parents=True, exist_ok=True)
        out_csv = DB_DIR / 'section7_anomaly_diag.csv'
        df.to_csv(out_csv, index=False)
        drop_csv = DB_DIR / 'section7_anomaly_dropped.csv'
        drop_df.to_csv(drop_csv, index=False)
        print(f'\nWrote {out_csv}')
        print(f'Wrote {drop_csv}')


if __name__ == '__main__':
    main()
