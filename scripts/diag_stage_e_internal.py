#!/usr/bin/env python3
"""Stage E debug helper — runs apply_corrections() on a case and then
runs network_conductivity AS A SUBPROCESS WITH STDOUT VISIBLE so the
NETWORK_DEBUG prints actually surface to the terminal.

Usage:
  python3 scripts/diag_stage_e_internal.py CASE_ID

This shows for each channel (ionic, e, thermal):
  - Per-mode V_source, G_eff, Σg_bulk, G/Σg ratio
  - Edge filter statistics (how many AM-AM dropped by MIN_FACTOR_CUTOFF)
  - Final σ_eff value
"""
from __future__ import annotations
import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / 'scripts'
WEBAPP = ROOT / 'webapp'
NET_PY = SCRIPTS / 'network_conductivity.py'

sys.path.insert(0, str(SCRIPTS))
from run_network_full_corrections import (   # noqa: E402
    apply_corrections, parse_type_map, _read_meta,
)


def find_case(case_id: str) -> Path | None:
    for base in ('results', 'archive'):
        root = WEBAPP / base
        if not root.exists():
            continue
        for atoms_p in root.rglob('atoms.csv'):
            if atoms_p.parent.name == case_id:
                return atoms_p.parent
    return None


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('case_id')
    ap.add_argument('--channel', choices=['ionic', 'e', 'kappa', 'all'],
                    default='all')
    args = ap.parse_args()

    case_dir = find_case(args.case_id)
    if not case_dir:
        ap.error(f'Case {args.case_id!r} not found')
    print(f'Case dir: {case_dir}')

    meta = _read_meta(case_dir)
    type_map = parse_type_map(meta.get('type_map', '1:AM_P,2:AM_S,3:SE'))
    if not type_map:
        type_map = {1: 'AM_P', 2: 'AM_S', 3: 'SE'}
    type_map_str = meta.get('type_map', '1:AM_P,2:AM_S,3:SE')
    scale = float(meta.get('scale', 1000))

    atoms = pd.read_csv(case_dir / 'atoms.csv')
    contacts = pd.read_csv(case_dir / 'contacts.csv', low_memory=False)
    print(f'  atoms     : {len(atoms)}')
    print(f'  contacts  : {len(contacts)}')

    df_ionic, df_e, df_kappa, factors = apply_corrections(
        atoms, contacts, type_map, scale)

    # Print factor stats
    print('\n=== apply_corrections() output ===')
    print(f'  factors_summary keys: {list(factors.keys())}')
    print(f'  r_SE_um           : {factors.get("r_SE_um")}')
    print(f'  f_SE_ionic        : {factors.get("f_SE_ionic")}')
    print(f'  AM_factors        : {factors.get("AM_factors")}')
    print(f'  fracture_stage    : {factors.get("fracture_stage_counts")}')
    print(f'  n_dropped (ionic/e/kappa) : '
          f'{factors.get("n_dropped_ionic")} / {factors.get("n_dropped_e")} / '
          f'{factors.get("n_dropped_kappa")}')
    print(f'  df sizes          : ionic={len(df_ionic)}  e={len(df_e)}  '
          f'kappa={len(df_kappa)}')

    channels = {'ionic': df_ionic, 'e': df_e, 'kappa': df_kappa}
    if args.channel != 'all':
        channels = {args.channel: channels[args.channel]}

    for name, df in channels.items():
        print(f'\n{"="*78}')
        print(f'  Channel: {name}')
        print('='*78)
        with tempfile.TemporaryDirectory(prefix=f'diag_{name}_') as tmpd:
            tmp = Path(tmpd)
            shutil.copy2(case_dir / 'atoms.csv', tmp / 'atoms.csv')
            df.to_csv(tmp / 'contacts.csv', index=False)
            for aux in ('input_params.json', 'meta.json'):
                src = case_dir / aux
                if src.exists():
                    shutil.copy2(src, tmp / aux)

            cmd = [sys.executable, str(NET_PY),
                   str(tmp / 'atoms.csv'), str(tmp / 'contacts.csv'),
                   '-o', str(tmp), '-t', type_map_str,
                   '-s', str(int(scale)),
                   '--contact-mode', 'hertzian']

            env = os.environ.copy()
            env['NETWORK_DEBUG'] = '1'

            # Capture but ALSO print
            cp = subprocess.run(cmd, env=env, capture_output=True,
                                  text=True, timeout=1800)
            # Print captured output directly
            for line in cp.stdout.splitlines():
                if any(k in line for k in
                       ('DEBUG', '⚠', 'σ', 'V_source', 'G_eff',
                        'iter', 'Solve', 'percolat',
                        'sigma_full', 'σ_full', 'Decomp', 'CONSTRICT',
                        'CONTACT', 'FULL', 'Bruggeman', 'Network')):
                    print(f'    {line}')
            if cp.returncode != 0:
                print(f'  ✗ subprocess returncode={cp.returncode}')
                if cp.stderr:
                    print(f'  stderr (last 500): ...{cp.stderr[-500:]}')
            else:
                # Try to read result
                json_p = tmp / 'network_conductivity.json'
                if json_p.exists():
                    res = json.load(open(json_p))
                    sf = res.get('sigma_full_mScm')
                    se = res.get('electronic_sigma_full_mScm')
                    sk = res.get('thermal_sigma_full_mScm')
                    print(f'\n  Result: σ_ionic={sf}  σ_e={se}  σ_th={sk}')


if __name__ == '__main__':
    main()
