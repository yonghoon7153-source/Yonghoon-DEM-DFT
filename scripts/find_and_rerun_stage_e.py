#!/usr/bin/env python3
"""Find cases needing Stage E re-run (r_SE not in size-invariant regime)
and re-run them with the literature-grounded σ_grain factors.

Triggers Stage E only on cases where σ_grain factor < 1.00, i.e. cases
with r_SE < 0.5 μm (transition + nano regime). Cases with r_SE ≥ 0.5 μm
have factor 1.00 → Stage E result identical to baseline → skip to save time.

Usage:
  python3 scripts/find_and_rerun_stage_e.py            # auto-find + run
  python3 scripts/find_and_rerun_stage_e.py --dry-run  # list only, don't run
  python3 scripts/find_and_rerun_stage_e.py --all      # force run all 78
"""
from __future__ import annotations
import argparse
import json
import subprocess
import sys
from pathlib import Path

import pandas as pd

ROOT     = Path(__file__).resolve().parent.parent
SCRIPTS  = ROOT / 'scripts'
WEBAPP   = ROOT / 'webapp'
STAGE_E  = SCRIPTS / 'run_network_full_corrections.py'

sys.path.insert(0, str(SCRIPTS))
from run_network_full_corrections import sigma_ionic_grain_factor_SE  # noqa: E402


def discover_case_dirs() -> list[Path]:
    out = []
    for base in ('results', 'archive'):
        root = WEBAPP / base
        if not root.exists(): continue
        for d in sorted(root.iterdir()):
            if (d.is_dir()
                    and (d / 'atoms.csv').exists()
                    and (d / 'full_metrics.json').exists()):
                out.append(d)
    return out


def _read_meta(case_dir: Path) -> dict:
    for path in (case_dir / 'meta.json',
                 WEBAPP / 'uploads' / case_dir.name / 'meta.json'):
        if path.exists():
            try: return json.load(open(path))
            except Exception: pass
    return {}


def _se_radius_real_um(case_dir: Path, meta: dict) -> float:
    p = case_dir / 'atoms.csv'
    if not p.exists():
        return float('nan')
    try:
        df = pd.read_csv(p, usecols=['type', 'radius'])
    except Exception:
        return float('nan')
    type_map_str = meta.get('type_map', '1:AM_P,2:AM_S,3:SE')
    se_types = []
    for tok in type_map_str.split(','):
        if ':' in tok:
            k, v = tok.split(':', 1)
            try:
                if 'SE' in v.strip():
                    se_types.append(int(k.strip()))
            except Exception:
                pass
    if not se_types:
        return float('nan')
    sub = df[df['type'].isin(se_types)]
    if sub.empty:
        return float('nan')
    scale = float(meta.get('scale', 1000))
    return float(sub['radius'].median()) * 1.0e6 / scale


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                  formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--dry-run', action='store_true', help='Print list, do not run')
    ap.add_argument('--all', action='store_true',
                     help='Run all (force, even size-invariant cases)')
    ap.add_argument('--threshold', type=float, default=0.99,
                     help='Skip cases whose σ_grain factor ≥ this (default 0.99)')
    args = ap.parse_args()

    cases = discover_case_dirs()
    print(f'Discovered {len(cases)} cases.\n', flush=True)

    needs_rerun = []
    skip = []
    for d in cases:
        meta = _read_meta(d)
        r_SE = _se_radius_real_um(d, meta)
        f = sigma_ionic_grain_factor_SE(r_SE)
        record = (d.name, r_SE, f)
        if args.all or f < args.threshold:
            needs_rerun.append(record)
        else:
            skip.append(record)

    print(f'Cases with σ_grain factor < {args.threshold:.2f} (need Stage E rerun):',
          flush=True)
    for cid, r, f in needs_rerun:
        print(f'  {cid:30s}  r_SE={r:.3f}μm  factor={f:.3f}', flush=True)
    print(f'\nCases at factor ≥ {args.threshold:.2f} (size-invariant, skip):  '
          f'{len(skip)}', flush=True)
    if not needs_rerun:
        print('\nNothing to re-run — all cases at size-invariant regime.', flush=True)
        return
    if args.dry_run:
        print('\n--dry-run: not executing.', flush=True)
        return

    print(f'\nExecuting Stage E on {len(needs_rerun)} cases…', flush=True)
    case_ids = [r[0] for r in needs_rerun]
    cmd = [sys.executable, str(STAGE_E)] + case_ids + ['--quiet']
    cp = subprocess.run(cmd)
    if cp.returncode == 0:
        print('Done.', flush=True)
    else:
        print(f'Stage E exited with code {cp.returncode}', flush=True)
        sys.exit(cp.returncode)


if __name__ == '__main__':
    main()
