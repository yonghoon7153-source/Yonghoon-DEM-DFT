#!/usr/bin/env python3
"""Backfill PHYS badge state in full_metrics.json from existing physics-mode
network solver outputs.

Why this exists
───────────────
The webapp index PHYS badge logic in app.py reads `physics_resistance_model`
from each case's full_metrics.json:

    'mikic' / 'maxwell+film' → PHYS ✓ (green)
    'maxwell' OR 'sigma_full_mScm_physics' present → PHYS legacy (orange)
    otherwise → PHYS ∅ (gray)

Many older cases ran the physics-mode solver (network_conductivity_physics.json
or network_conductivity_dual.json present in the case dir) but the merge step
that writes `physics_resistance_model` + the `_physics`-suffixed σ keys never
ran, so their badges show ∅ even though the physics data exists on disk.

This is a one-shot backfill: scan every case dir, look for physics solver
output, merge the σ keys + write `physics_resistance_model` and
`physics_solver_at` into full_metrics.json. Idempotent — re-running on
already-backfilled cases changes nothing.

Usage:
  python3 scripts/backfill_phys_badge.py                 # all cases
  python3 scripts/backfill_phys_badge.py --quiet         # one summary line
  python3 scripts/backfill_phys_badge.py CASE_ID …       # specific cases
"""
from __future__ import annotations
import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path

ROOT   = Path(__file__).resolve().parent.parent
WEBAPP = ROOT / 'webapp'

# Same key remap the webapp uses in /analyze step 3 (app.py ~line 2116).
PHYS_REMAP = [
    ('sigma_full',                 'sigma_full_physics'),
    ('sigma_full_mScm',            'sigma_full_mScm_physics'),
    ('sigma_bulk_net',             'sigma_bulk_net_physics'),
    ('sigma_bulk_net_mScm',        'sigma_bulk_net_mScm_physics'),
    ('R_brug_over_full',           'R_brug_over_full_physics'),
    ('bulk_resistance_fraction',   'bulk_resistance_fraction_physics'),
    ('electronic_sigma_full_mScm', 'electronic_sigma_full_mScm_physics'),
    ('thermal_sigma_full_mScm',    'thermal_sigma_full_mScm_physics'),
]


def discover_case_dirs() -> list[Path]:
    """Recursively find case dirs at any depth under results/ or archive/."""
    seen = set()
    out = []
    for base in ('results', 'archive'):
        root = WEBAPP / base
        if not root.exists():
            continue
        for fm_p in root.rglob('full_metrics.json'):
            case_dir = fm_p.parent
            if case_dir not in seen:
                seen.add(case_dir)
                out.append(case_dir)
    return sorted(out)


def _load_phys_data(case_dir: Path) -> tuple[dict, str]:
    """Return (phys_data, source) — first available physics solver output."""
    p = case_dir / 'network_conductivity_physics.json'
    if p.exists():
        try:
            return json.load(open(p)), 'network_conductivity_physics.json'
        except Exception:
            pass
    p = case_dir / 'network_conductivity_dual.json'
    if p.exists():
        try:
            d = json.load(open(p))
            if isinstance(d, dict) and isinstance(d.get('physics'), dict):
                return d['physics'], 'network_conductivity_dual.json:physics'
        except Exception:
            pass
    return {}, ''


def backfill_one(case_dir: Path) -> tuple[str, str, str]:
    """Return (case_id, status, message). status ∈ {'updated','skipped','no-phys'}."""
    fm_path = case_dir / 'full_metrics.json'
    try:
        with open(fm_path) as f:
            fm = json.load(f)
    except Exception as e:
        return (case_dir.name, 'error', f'fm read failed: {e}')

    cur_model = fm.get('physics_resistance_model')

    # Already in the upgraded state — nothing to do.
    if cur_model in ('mikic', 'maxwell+film'):
        return (case_dir.name, 'skipped', f'already PHYS ✓ ({cur_model})')

    phys_data, source = _load_phys_data(case_dir)

    # No physics solver output exists at all → must rerun /analyze, not backfill.
    if not phys_data:
        # Last-ditch: maybe sigma_full_mScm_physics already in fm but model
        # tag missing — that becomes 'maxwell' (legacy) automatically via the
        # webapp logic, so still write a tag so the badge stops being ∅.
        if 'sigma_full_mScm_physics' in fm:
            fm['physics_resistance_model'] = 'maxwell'
            if not fm.get('physics_solver_at'):
                ts = datetime.fromtimestamp(fm_path.stat().st_mtime).strftime(
                    '%Y-%m-%d %H:%M:%S')
                fm['physics_solver_at'] = ts
            with open(fm_path, 'w') as f:
                json.dump(fm, f, indent=2, default=str)
            return (case_dir.name, 'updated',
                    'tagged maxwell (only _physics keys present, no JSON)')
        return (case_dir.name, 'no-phys',
                'no physics solver output (rerun /analyze)')

    # Merge _physics-suffixed σ keys (idempotent — overwrites with same value).
    n_merged = 0
    for src, dst in PHYS_REMAP:
        v = phys_data.get(src)
        if v is not None:
            fm[dst] = v
            n_merged += 1

    # Set the badge tag — prefer the model declared by the solver itself.
    new_model = phys_data.get('resistance_model') or 'maxwell+film'
    fm['physics_resistance_model'] = new_model

    # Timestamp from the physics JSON file mtime (more honest than "now").
    src_path = case_dir / source.split(':', 1)[0]
    if src_path.exists():
        ts = datetime.fromtimestamp(src_path.stat().st_mtime).strftime(
            '%Y-%m-%d %H:%M:%S')
    else:
        ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    fm['physics_solver_at'] = ts

    with open(fm_path, 'w') as f:
        json.dump(fm, f, indent=2, default=str)

    badge = 'PHYS ✓' if new_model in ('mikic', 'maxwell+film') else 'PHYS legacy'
    return (case_dir.name, 'updated',
            f'{badge} model={new_model} keys={n_merged} from {source}')


def main() -> None:
    ap = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=__doc__)
    ap.add_argument('cases', nargs='*', help='Specific case_ids')
    ap.add_argument('--quiet', action='store_true',
                    help='Only print the final summary line')
    args = ap.parse_args()

    all_cases = discover_case_dirs()
    if args.cases:
        wanted = set(args.cases)
        cases = [d for d in all_cases if d.name in wanted]
    else:
        cases = all_cases
    if not cases:
        ap.error('No cases found.')

    if not args.quiet:
        print(f'PHYS badge backfill on {len(cases)} cases …', flush=True)
    n_upd = n_skip = n_none = n_err = 0
    for i, d in enumerate(cases, 1):
        cid, status, msg = backfill_one(d)
        if status == 'updated':   n_upd += 1; tag = '✓'
        elif status == 'skipped': n_skip += 1; tag = '·'
        elif status == 'no-phys': n_none += 1; tag = '∅'
        else:                     n_err += 1; tag = '✗'
        if not args.quiet:
            print(f'  [{i:3d}/{len(cases)}] {tag} {cid:30s}  {msg[:120]}',
                  flush=True)
    print(f'\nDone — {n_upd} updated, {n_skip} already PHYS ✓, '
          f'{n_none} no physics output, {n_err} errors.',
          flush=True)
    if n_none and not args.quiet:
        print('  → cases marked "no physics output" need /analyze rerun '
              '(전체 재분석 NET 강제) to produce network_conductivity_physics.json.')


if __name__ == '__main__':
    main()
