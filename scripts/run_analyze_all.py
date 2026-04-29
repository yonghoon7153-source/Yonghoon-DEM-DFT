#!/usr/bin/env python3
"""Re-run analyze_contacts.py over every case in webapp/results and
webapp/archive, picking up the per-case meta.json (type_map, scale)
automatically.

Usage:
  python3 scripts/run_analyze_all.py                # all cases
  python3 scripts/run_analyze_all.py --quiet        # one summary line per case
  python3 scripts/run_analyze_all.py CASE_ID ...    # specific cases only
  python3 scripts/run_analyze_all.py --jobs 4       # parallel workers

Why this exists
───────────────
analyze_contacts.py takes two positional args (atoms_csv, contacts_csv)
plus a -t type_map and -s scale. A naive `for d in webapp/results/*`
loop that passes only the directory fails; this wrapper does the
correct unpacking from meta.json so Tier-1 patches (B3 / C4 / F1 / F2)
actually get re-applied to every case's full_metrics.json.
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
ANALYZE = ROOT / 'scripts' / 'analyze_contacts.py'


def discover_cases() -> list[Path]:
    out = []
    for base in ('results', 'archive'):
        root = WEBAPP / base
        if root.exists():
            for d in sorted(root.iterdir()):
                if (d.is_dir()
                        and (d / 'atoms.csv').exists()
                        and (d / 'contacts.csv').exists()):
                    out.append(d)
    return out


def _read_meta(case_dir: Path) -> dict:
    for path in (case_dir / 'meta.json',
                 WEBAPP / 'uploads' / case_dir.name / 'meta.json'):
        if path.exists():
            try:
                return json.load(open(path))
            except Exception:
                pass
    return {}


def run_one(case_dir: Path, quiet: bool = False) -> tuple[str, bool, str]:
    meta = _read_meta(case_dir)
    type_map = meta.get('type_map', '1:AM_P,2:AM_S,3:SE')
    scale = str(meta.get('scale', 1000))
    cmd = [
        sys.executable, str(ANALYZE),
        str(case_dir / 'atoms.csv'),
        str(case_dir / 'contacts.csv'),
        '-o', str(case_dir),
        '-t', type_map,
        '-s', scale,
    ]
    try:
        cp = subprocess.run(cmd, check=False, capture_output=True, text=True,
                             timeout=600)
        ok = (cp.returncode == 0)
        msg = (cp.stdout or '').strip().splitlines()
        last = msg[-1] if msg else ''
        if cp.returncode != 0:
            err_lines = (cp.stderr or '').strip().splitlines()
            last = (err_lines[-1] if err_lines else
                    f'returncode={cp.returncode}')
        return (case_dir.name, ok, last)
    except Exception as e:
        return (case_dir.name, False, f'EXC: {e}')


def main() -> None:
    ap = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                  description=__doc__)
    ap.add_argument('cases', nargs='*', help='Specific case_ids (default: all)')
    ap.add_argument('--quiet', action='store_true',
                    help='One summary line per case')
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

    print(f'Running analyze_contacts on {len(cases)} cases '
          f'(jobs={args.jobs}) ...', flush=True)
    n_ok = n_fail = 0

    if args.jobs > 1:
        with ProcessPoolExecutor(max_workers=args.jobs) as ex:
            futs = {ex.submit(run_one, d, args.quiet): d for d in cases}
            for i, f in enumerate(as_completed(futs), 1):
                cid, ok, last = f.result()
                tag = '✓' if ok else '✗'
                if not args.quiet or not ok:
                    print(f'  [{i:3d}/{len(cases)}] {tag} {cid:30s}  {last[:80]}',
                          flush=True)
                if ok: n_ok += 1
                else:  n_fail += 1
    else:
        for i, d in enumerate(cases, 1):
            cid, ok, last = run_one(d, args.quiet)
            tag = '✓' if ok else '✗'
            if not args.quiet or not ok:
                print(f'  [{i:3d}/{len(cases)}] {tag} {cid:30s}  {last[:80]}',
                      flush=True)
            if ok: n_ok += 1
            else:  n_fail += 1

    print(f'\nDone — {n_ok} ok, {n_fail} failed.', flush=True)
    if n_fail:
        sys.exit(1)


if __name__ == '__main__':
    main()
