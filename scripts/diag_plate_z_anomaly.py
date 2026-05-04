"""Compare plate_z and node-distribution stats between anomaly vs clean case.

Diagnoses whether the σ-inflation in 22 anomaly cases is caused by the
plate_z fallback `max(z of particles)` overshooting due to stray boundary
particles, vs the actual physical pellet height.

Usage:
  python3 scripts/diag_plate_z_anomaly.py
"""
from __future__ import annotations
import json
import os
import sys
from pathlib import Path

import pandas as pd

ROOT   = Path(__file__).resolve().parent.parent
WEBAPP = ROOT / 'webapp'

# Three anomaly + three clean cases for comparison
CASES = {
    'anomaly_115455_8c26b6':   'results/260420_115455_8c26b6',
    'anomaly_213836_aeccd4':   'results/260421_213836_aeccd4',
    'anomaly_214401_3611fe':   'results/260421_214401_3611fe',
    'clean_212704_8d08ed':     'results/260421_212704_8d08ed',
    'clean_213505_8b88bf':     'results/260421_213505_8b88bf',
    'clean_192638_5ebcec':     'results/260421_192638_5ebcec',
}


def main() -> None:
    print(f'{"case":35s} {"n_atoms":>9s} {"max_z":>10s} {"p99_z":>10s} '
          f'{"max/p99":>9s} {"box_z":>10s} {"mesh_pz":>10s}')
    print('-' * 100)
    for name, sub in CASES.items():
        d = WEBAPP / sub
        if not d.exists():
            print(f'{name:35s}  <not found>')
            continue
        atoms = pd.read_csv(d / 'atoms.csv', usecols=['type', 'z', 'radius'])
        n = len(atoms)
        max_z = atoms['z'].max()
        p99_z = atoms['z'].quantile(0.99)
        ratio = max_z / p99_z if p99_z > 0 else float('inf')

        ip = d / 'input_params.json'
        box_z = '?'
        if ip.exists():
            with open(ip) as f:
                box_z = json.load(f).get('box_z', '?')

        mi = d / 'mesh_info.json'
        mesh_pz = '?'
        if mi.exists():
            with open(mi) as f:
                mesh_pz = json.load(f).get('plate_z', '?')

        box_z_str = f'{box_z:.5f}' if isinstance(box_z, (int, float)) else str(box_z)
        mesh_pz_str = (f'{mesh_pz:.5f}' if isinstance(mesh_pz, (int, float))
                       else str(mesh_pz))
        print(f'{name:35s} {n:>9d} {max_z:>10.5f} {p99_z:>10.5f} '
              f'{ratio:>9.3f} {box_z_str:>10s} {mesh_pz_str:>10s}')

    print('\n  → If anomaly cases have max_z >> p99_z (ratio >> 1), the')
    print('    fallback plate_z = max(z) overshoots due to a stray boundary')
    print('    particle and inflates T_um → inflates σ_ratio.')
    print('  → If anomaly cases have mesh_info.json plate_z very different')
    print('    from box_z, that mesh value may be the source of inflation.')


if __name__ == '__main__':
    main()
