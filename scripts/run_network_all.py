#!/usr/bin/env python3
"""Re-run network_conductivity.py over every case and merge results into
full_metrics.json. Companion to run_analyze_all.py — call after
analyze_contacts has populated the basic full_metrics.json fields, and
this script then adds sigma_full_mScm, sigma_bulk_net_mScm,
electronic_sigma_full_mScm, network_solver_status, etc. that the webapp
/analyze pipeline normally appends as a separate step.

Usage:
  python3 scripts/run_network_all.py                  # all cases
  python3 scripts/run_network_all.py --quiet          # one line per case
  python3 scripts/run_network_all.py CASE_ID ...      # specific cases
  python3 scripts/run_network_all.py --jobs 4         # parallel workers

Why
───
analyze_contacts.py writes full_metrics.json in 'w' mode, which means
any sigma_* keys previously written by network_conductivity.py are
overwritten and lost. The webapp avoids this by always running both
in sequence; manual Stage A loops have no such safeguard. This wrapper
restores parity.
"""
from __future__ import annotations
import argparse
import json
import os
import subprocess
import sys
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WEBAPP = ROOT / 'webapp'
NET_SCRIPT = ROOT / 'scripts' / 'network_conductivity.py'


# Keys to merge from network_conductivity.json → full_metrics.json
# (mirror of webapp/app.py:_NET_MERGE_KEYS)
_NET_MERGE_KEYS = [
    'sigma_full', 'sigma_full_mScm',
    'sigma_bulk_net', 'sigma_bulk_net_mScm',
    'sigma_bruggeman', 'sigma_bruggeman_mScm',
    'R_brug_over_full', 'R_bruggeman_over_full',
    'bulk_resistance_fraction',
    'electronic_sigma_full_mScm', 'electronic_R_brug',
    'electronic_active_fraction', 'electronic_percolating_fraction',
    'thermal_sigma_full_mScm', 'thermal_R_brug',
    'physics_resistance_model', 'physics_solver_at',
    # ── Physics-mode (Tabor + volume) counterparts ──
    # network_conductivity.py emits these when called with
    # --contact-mode both; without them, Stage E sees Physics baseline
    # as 0/None and the UI Physics column shows '—'.
    'sigma_full_physics', 'sigma_full_mScm_physics',
    'sigma_bulk_net_physics', 'sigma_bulk_net_mScm_physics',
    'electronic_sigma_full_mScm_physics',
    'thermal_sigma_full_mScm_physics',
    'bulk_resistance_fraction_physics',
    'R_brug_over_full_physics',
]


def discover_cases() -> list[Path]:
    """Recursively find all case directories under results/ and archive/.

    A case is any directory containing both atoms.csv and contacts.csv.
    rglob() walks arbitrary depth, so categorized archive folders like
    `webapp/archive/후막(6mAh)/input_6mAh_real_3/` (depth 2) are
    discovered, not just depth-1 newly-uploaded cases. Without this,
    stage scripts silently skipped 50+ % of the dataset.
    """
    seen = set()
    out = []
    for base in ('results', 'archive'):
        root = WEBAPP / base
        if not root.exists(): continue
        for atoms_p in root.rglob('atoms.csv'):
            case_dir = atoms_p.parent
            if (case_dir / 'contacts.csv').exists() and case_dir not in seen:
                seen.add(case_dir)
                out.append(case_dir)
    return sorted(out)


def _read_meta(case_dir: Path) -> dict:
    for path in (case_dir / 'meta.json',
                 WEBAPP / 'uploads' / case_dir.name / 'meta.json'):
        if path.exists():
            try:
                return json.load(open(path))
            except Exception:
                pass
    return {}


def run_one(case_dir: Path) -> tuple[str, bool, str]:
    meta = _read_meta(case_dir)
    type_map = meta.get('type_map', '1:AM_P,2:AM_S,3:SE')
    scale = str(meta.get('scale', 1000))
    cmd = [
        sys.executable, str(NET_SCRIPT),
        str(case_dir / 'atoms.csv'),
        str(case_dir / 'contacts.csv'),
        '-o', str(case_dir),
        '-t', type_map,
        '-s', scale,
        '--contact-mode', 'both',
    ]
    try:
        cp = subprocess.run(cmd, check=False, capture_output=True, text=True,
                             timeout=1800)
        ok = (cp.returncode == 0)
        if not ok:
            err = (cp.stderr or '').strip().splitlines()
            last = err[-1] if err else f'returncode={cp.returncode}'
            return (case_dir.name, False, last[:120])
    except Exception as e:
        return (case_dir.name, False, f'EXC: {e}')

    # Merge network_conductivity.json → full_metrics.json
    net_json = case_dir / 'network_conductivity.json'
    fm_json  = case_dir / 'full_metrics.json'
    if not net_json.exists():
        return (case_dir.name, False, 'no network_conductivity.json output')
    if not fm_json.exists():
        return (case_dir.name, False, 'no full_metrics.json to merge into')
    try:
        with open(net_json) as f:
            net_data = json.load(f)
        with open(fm_json) as f:
            fm_data = json.load(f)
        merged_keys = []
        for k in _NET_MERGE_KEYS:
            if k in net_data and net_data[k] is not None:
                fm_data[k] = net_data[k]
                merged_keys.append(k)
        fm_data['network_solver_status'] = 'success'
        with open(fm_json, 'w') as f:
            json.dump(fm_data, f, indent=2, default=str)
        sigma_v = fm_data.get('sigma_full_mScm', '?')
        return (case_dir.name, True,
                f'σ_full={sigma_v} mScm  ({len(merged_keys)} keys merged)')
    except Exception as e:
        return (case_dir.name, False, f'merge failed: {e}')


def main() -> None:
    ap = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                  description=__doc__)
    ap.add_argument('cases', nargs='*', help='Specific case_ids (default: all)')
    ap.add_argument('--quiet', action='store_true',
                    help='One line per case')
    ap.add_argument('--jobs', '-j', type=int, default=1,
                    help='Parallel workers (default 1)')
    args = ap.parse_args()

    all_cases = discover_cases()
    if args.cases:
        wanted = set(args.cases)
        cases = [d for d in all_cases if d.name in wanted]
    else:
        cases = all_cases

    if not cases:
        ap.error('No cases found.')

    print(f'Running network_conductivity on {len(cases)} cases '
          f'(jobs={args.jobs}) …', flush=True)
    n_ok = n_fail = 0

    if args.jobs > 1:
        with ProcessPoolExecutor(max_workers=args.jobs) as ex:
            futs = {ex.submit(run_one, d): d for d in cases}
            for i, f in enumerate(as_completed(futs), 1):
                cid, ok, msg = f.result()
                tag = '✓' if ok else '✗'
                if not args.quiet or not ok:
                    print(f'  [{i:3d}/{len(cases)}] {tag} {cid:30s}  {msg[:90]}',
                          flush=True)
                if ok: n_ok += 1
                else:  n_fail += 1
    else:
        for i, d in enumerate(cases, 1):
            cid, ok, msg = run_one(d)
            tag = '✓' if ok else '✗'
            if not args.quiet or not ok:
                print(f'  [{i:3d}/{len(cases)}] {tag} {cid:30s}  {msg[:90]}',
                      flush=True)
            if ok: n_ok += 1
            else:  n_fail += 1

    print(f'\nDone — {n_ok} ok, {n_fail} failed.', flush=True)
    if n_fail:
        sys.exit(1)


if __name__ == '__main__':
    main()
