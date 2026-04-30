#!/usr/bin/env python3
"""Backfill fracture-stage keys from b2_b4_diagnostic.csv into per-case
full_metrics.json files.

Why this exists
───────────────
The auto-DB pipeline (commit fe69669) integrated calc_fracture_stages
into run_full_analysis, so future analyze_contacts runs write fracture
keys (n_*_AM_AM, frac_*_pct, fracture_index, R_min_um_median_*, ...)
directly into full_metrics.json. Cases analysed BEFORE that commit have
the fracture data only in b2_b4_diagnostic.csv (master-DB-only) and
not in their own full_metrics.json — so the new Fracture Analysis tab
in the webapp returns None for them.

This script is a one-shot bridge: read b2_b4_diagnostic.csv, find each
case's row, and merge those columns into the corresponding
full_metrics.json under the same flat keys. Idempotent — running it
again on already-backfilled cases is a no-op.

Usage:
  python3 scripts/backfill_fracture_keys.py            # all cases
  python3 scripts/backfill_fracture_keys.py CASE_ID …  # specific cases
"""
from __future__ import annotations
import argparse
import json
import math
import sys
from pathlib import Path

import pandas as pd

ROOT  = Path(__file__).resolve().parent.parent
WEBAPP = ROOT / 'webapp'
B2B4_CSV = ROOT / 'docs' / 'figures' / 'physics_regime' / 'b2_b4_diagnostic.csv'


# Keys to copy from b2_b4_diagnostic.csv → full_metrics.json. These are
# exactly the columns calc_fracture_stages emits in the auto-DB pipeline.
FRACTURE_KEYS_PREFIXES = [
    'n_intact_AM_AM', 'n_microcrack_AM_AM', 'n_multicrack_AM_AM',
    'n_fragmentation_AM_AM', 'n_pulverization_AM_AM',
    'n_intact_force_AM_AM', 'n_microcrack_force_AM_AM',
    'n_multicrack_force_AM_AM', 'n_fragmentation_force_AM_AM',
    'n_pulverization_force_AM_AM',
    'n_total_AM_AM', 'n_total_AM_AM_force',
    'frac_intact_pct', 'frac_microcrack_pct', 'frac_multicrack_pct',
    'frac_fragmentation_pct', 'frac_pulverization_pct',
    'frac_intact_force_pct', 'frac_microcrack_force_pct',
    'frac_multicrack_force_pct', 'frac_fragmentation_force_pct',
    'frac_pulverization_force_pct',
    'fracture_index', 'fracture_index_force',
]
# Per-pair-type breakdown columns: n_*_<pair>, frac_*_<pair>_pct,
# n_total_<pair>, R_min_um_median_<pair>, P_c_mN_median_<pair>,
# F_mN_median_<pair>, F_over_Pc_median_<pair> for AM_P-AM_P, AM_S-AM_S, AM_P-AM_S
PAIR_TYPES = ['AM_P-AM_P', 'AM_S-AM_S', 'AM_P-AM_S']
STAGES = ['intact', 'microcrack', 'multicrack', 'fragmentation', 'pulverization']
for pt in PAIR_TYPES:
    for s in STAGES:
        FRACTURE_KEYS_PREFIXES += [
            f'n_{s}_{pt}', f'frac_{s}_{pt}_pct',
            f'n_{s}_force_{pt}', f'frac_{s}_force_{pt}_pct',
        ]
    FRACTURE_KEYS_PREFIXES += [
        f'n_total_{pt}', f'n_total_force_{pt}',
        f'R_min_um_median_{pt}', f'P_c_mN_median_{pt}',
        f'F_mN_median_{pt}', f'F_over_Pc_median_{pt}',
    ]
# Dedup
FRACTURE_KEYS = sorted(set(FRACTURE_KEYS_PREFIXES))


def discover_case_dirs() -> dict[str, Path]:
    """case_id → case directory containing full_metrics.json."""
    out = {}
    for base in ('results', 'archive'):
        root = WEBAPP / base
        if not root.exists(): continue
        for d in sorted(root.iterdir()):
            if d.is_dir() and (d / 'full_metrics.json').exists():
                out[d.name] = d
    return out


def _is_nan(v) -> bool:
    try:
        return math.isnan(float(v))
    except (TypeError, ValueError):
        return False


def main() -> None:
    ap = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                  description=__doc__)
    ap.add_argument('cases', nargs='*', help='Specific case_ids (default: all)')
    args = ap.parse_args()

    if not B2B4_CSV.exists():
        sys.exit(f'b2_b4_diagnostic.csv not found at {B2B4_CSV}\n'
                 f'Run b2_b4_diagnostic.py first.')
    df = pd.read_csv(B2B4_CSV)
    if 'case_id' not in df.columns:
        sys.exit('b2_b4_diagnostic.csv has no case_id column')
    df = df.set_index('case_id')

    case_dirs = discover_case_dirs()
    if args.cases:
        wanted = set(args.cases)
        case_dirs = {k: v for k, v in case_dirs.items() if k in wanted}

    available_keys = [k for k in FRACTURE_KEYS if k in df.columns]
    print(f'Backfilling {len(available_keys)} fracture keys '
          f'into {len(case_dirs)} cases …', flush=True)
    n_ok = n_skip = n_missing = 0
    for cid, case_dir in case_dirs.items():
        if cid not in df.index:
            n_missing += 1
            continue
        row = df.loc[cid]
        if isinstance(row, pd.DataFrame):  # duplicates → take first
            row = row.iloc[0]
        fm_path = case_dir / 'full_metrics.json'
        try:
            with open(fm_path) as f:
                fm = json.load(f)
        except Exception as e:
            print(f'  ✗ {cid}: read failed ({e})', flush=True)
            n_skip += 1
            continue
        # Check if already backfilled (no overwrite if any fracture key already present)
        if 'fracture_index' in fm and fm.get('fracture_index') is not None:
            n_skip += 1
            continue
        added = 0
        for k in available_keys:
            v = row.get(k)
            if v is None or _is_nan(v):
                continue
            # Convert numpy int/float → Python types for JSON
            try:
                if isinstance(v, (int, bool)):
                    fm[k] = v
                elif isinstance(v, float):
                    fm[k] = round(float(v), 6)
                else:
                    fm[k] = v
            except Exception:
                fm[k] = v
            added += 1
        with open(fm_path, 'w') as f:
            json.dump(fm, f, indent=2, default=str)
        print(f'  ✓ {cid:30s}  {added:3d} keys backfilled', flush=True)
        n_ok += 1
    print(f'\nDone — {n_ok} backfilled, {n_skip} skipped (already done), '
          f'{n_missing} missing in CSV.', flush=True)


if __name__ == '__main__':
    main()
