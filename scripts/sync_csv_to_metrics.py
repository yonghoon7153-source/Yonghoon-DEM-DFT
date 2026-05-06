#!/usr/bin/env python3
"""Sync σ_e and κ values from network_summary.csv into full_metrics.json.

Some cases (~17 in current ensemble) have stale full_metrics.json with
inflated σ_e / κ baseline values left over from pre-Layer-1 buggy runs.
The CSV (network_summary.csv), being written by a later run of analyze_
contacts.py, has the correct values.

This script reconciles the two by overwriting full_metrics.json's
electronic_sigma_full_mScm and thermal_sigma_full_mScm fields (and
their _physics variants) from the CSV. After running it, re-run Stage E
to recompute fallback values against the corrected baselines.

Usage:
    python3 scripts/sync_csv_to_metrics.py            # all cases, sync only mismatched
    python3 scripts/sync_csv_to_metrics.py --dry-run  # report only, no writes
    python3 scripts/sync_csv_to_metrics.py --threshold 0.05  # mismatch >5%
    python3 scripts/sync_csv_to_metrics.py CASE_ID    # one case

After running:
    bash scripts/run all-stagee <fixed cases>
"""
from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path


CSV_KEY_TO_JSON_KEY = {
    'σ_ionic (mS/cm)':                     'sigma_full_mScm',
    'σ_electronic (mS/cm)':                'electronic_sigma_full_mScm',
    'σ_thermal (mS/cm equiv)':             'thermal_sigma_full_mScm',
    'σ_ionic [physics] (mS/cm)':           'sigma_full_mScm_physics',
    'σ_electronic [physics] (mS/cm)':      'electronic_sigma_full_mScm_physics',
    'σ_thermal [physics] (mS/cm equiv)':   'thermal_sigma_full_mScm_physics',
}


def _read_csv_values(csv_path: Path) -> dict:
    """Read network_summary.csv and return {csv_label: float}."""
    out = {}
    with open(csv_path) as f:
        for line in f:
            line = line.rstrip('\n').rstrip('\r')
            if ',' not in line:
                continue
            label, _, rest = line.partition(',')
            label = label.strip()
            if label in CSV_KEY_TO_JSON_KEY:
                try:
                    out[label] = float(rest.split(',')[0])
                except (ValueError, IndexError):
                    pass
    return out


def _sync_one(case_dir: Path, threshold: float = 0.05, dry_run: bool = False
              ) -> tuple[str, list[tuple[str, float, float]]]:
    """Return (status, list of (key, old_json_val, csv_val) for changed keys)."""
    fm_path = case_dir / 'full_metrics.json'
    csv_path = case_dir / 'network_summary.csv'
    if not (fm_path.exists() and csv_path.exists()):
        return ('skip', [])

    csv_vals = _read_csv_values(csv_path)
    if not csv_vals:
        return ('no_csv_keys', [])

    with open(fm_path) as f:
        fm = json.load(f)

    changes = []
    for csv_label, val in csv_vals.items():
        json_key = CSV_KEY_TO_JSON_KEY[csv_label]
        old = fm.get(json_key)
        if old is None:
            continue
        if val == 0:
            continue
        ratio = old / val if val else 0
        if abs(ratio - 1.0) > threshold:
            changes.append((json_key, old, val))

    if not changes:
        return ('ok', [])

    if not dry_run:
        for k, _, v in changes:
            fm[k] = v
        with open(fm_path, 'w') as f:
            json.dump(fm, f, indent=2, default=str)

    return ('synced' if not dry_run else 'would_sync', changes)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('case_id', nargs='?',
                    help='Specific case_id (else scans all)')
    ap.add_argument('--threshold', type=float, default=0.05,
                    help='Relative-error threshold for mismatch (default 5%%)')
    ap.add_argument('--dry-run', action='store_true',
                    help='Report only, do not modify files')
    args = ap.parse_args()

    root = Path('webapp')
    cases = []
    for fm in root.rglob('full_metrics.json'):
        case_dir = fm.parent
        if args.case_id and case_dir.name != args.case_id:
            continue
        cases.append(case_dir)

    if not cases:
        print('No cases found.')
        return

    print(f'Scanning {len(cases)} cases (threshold {args.threshold*100:.0f}%, '
          f'dry-run={args.dry_run})...\n')

    n_synced = 0
    n_ok = 0
    fixed_case_ids = []
    for case_dir in sorted(cases):
        status, changes = _sync_one(case_dir, args.threshold, args.dry_run)
        if status in ('ok', 'skip', 'no_csv_keys'):
            n_ok += 1
            continue
        n_synced += 1
        fixed_case_ids.append(case_dir.name)
        prefix = '✓' if status == 'synced' else '⚠ would-sync'
        print(f'{prefix}  {case_dir.name}')
        for k, old, new in changes:
            ratio = old / new if new else 0
            print(f'    {k:40s}  {old:>10.3f}  →  {new:>10.3f}  '
                  f'(was {ratio:.1f}× CSV)')

    print(f'\nDone — {n_synced} cases synced, {n_ok} already-OK.')
    if n_synced and not args.dry_run:
        print('\nNext step: re-run Stage E for the fixed cases:')
        print(f"  bash scripts/run all-stagee {' '.join(fixed_case_ids)}")


if __name__ == '__main__':
    main()
