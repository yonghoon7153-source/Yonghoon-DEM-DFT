#!/usr/bin/env python
"""make_v0_dft_input.py — build a V0 DFT relax.in from the VERIFIED DFT+U/ISPIN
template + a UMA champion cif, scaled to the ensemble V0.

Keeps the template's namelists, ATOMIC_SPECIES, HUBBARD, K_POINTS verbatim
(so DFT+U(8 eV ortho-atomic) + ISPIN=2 + Nd1/Nd2 AFM are preserved); replaces
ONLY CELL_PARAMETERS (scaled to V0) and ATOMIC_POSITIONS (champion coords, the
two Nd labeled Nd1/Nd2 to match the template species). Also renames prefix.

  python3 make_v0_dft_input.py \
      --template pair01_pair_00_reference_1_82/v100/relax.in \
      --cif uma_eos_ens/rank1_seed2_relaxed.cif \
      --v0 2399.07 --prefix nd_pair01_v0 \
      --out pair01_pair_00_reference_1_82/v0_champion/relax.in
"""
import argparse
import os
from ase.io import read


def _is_pos_line(s):
    p = s.split()
    if len(p) < 4 or not p[0][0].isalpha():
        return False
    try:
        float(p[1]); float(p[2]); float(p[3])
        return True
    except ValueError:
        return False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--template', required=True, help='verified relax.in (+U/ISPIN, Nd1/Nd2)')
    ap.add_argument('--cif', required=True, help='UMA champion relaxed cif')
    ap.add_argument('--v0', type=float, required=True, help='target V0 (Å³)')
    ap.add_argument('--prefix', default='nd_pair01_v0', help='QE prefix for the new run')
    ap.add_argument('--out', required=True)
    a = ap.parse_args()

    atoms = read(a.cif)
    V = atoms.get_volume()
    scale = (a.v0 / V) ** (1.0 / 3.0)
    cell = atoms.cell.array * scale
    frac = atoms.get_scaled_positions()
    syms = atoms.get_chemical_symbols()

    nd = 0
    labels = []
    for s in syms:
        if s == 'Nd':
            nd += 1
            labels.append(f'Nd{nd}')
        else:
            labels.append(s)
    if nd != 2:
        raise SystemExit(f'expected exactly 2 Nd in {a.cif}, found {nd}')

    tl = open(a.template).read().splitlines()
    out, i, n = [], 0, len(tl)
    while i < n:
        ln = tl[i]
        key = ln.strip().upper()
        if ln.strip().startswith('prefix'):
            out.append(f"    prefix      = '{a.prefix}'")
            i += 1
            continue
        if key.startswith('CELL_PARAMETERS'):
            out.append('CELL_PARAMETERS angstrom')
            for k in range(3):
                out.append(f'  {cell[k,0]:18.12f}  {cell[k,1]:18.12f}  {cell[k,2]:18.12f}')
            i += 1
            skipped = 0
            while i < n and skipped < 3:   # skip template's 3 cell vectors
                if tl[i].split():
                    skipped += 1
                i += 1
            continue
        if key.startswith('ATOMIC_POSITIONS'):
            out.append('ATOMIC_POSITIONS (crystal)')
            for lab, p in zip(labels, frac):
                out.append(f'  {lab:<5} {p[0]:18.12f}  {p[1]:18.12f}  {p[2]:18.12f}')
            i += 1
            while i < n and _is_pos_line(tl[i]):  # skip template's position lines
                i += 1
            continue
        out.append(ln)
        i += 1

    os.makedirs(os.path.dirname(a.out) or '.', exist_ok=True)
    open(a.out, 'w').write('\n'.join(out) + '\n')
    print(f'wrote {a.out}')
    print(f'  V0={a.v0:.2f} Å³  scale={scale:.6f} (from V_ref={V:.2f})  natoms={len(labels)}  Nd1/Nd2 labeled')
    print(f'  prefix={a.prefix}')


if __name__ == '__main__':
    main()
