"""qe_relax_to_xyz.py — convert QE relax.out last frame to extxyz.

Pure stdlib (no ase). Reads CELL_PARAMETERS (angstrom) from relax.in
and last ATOMIC_POSITIONS block from relax.out, converts fractional
coords to cartesian, writes extxyz.

Usage:
  python3 qe_relax_to_xyz.py relax.in relax.out output.xyz
  # or with defaults (relax.in + relax.out in CWD)
  python3 qe_relax_to_xyz.py
"""
import re
import sys
from pathlib import Path


def parse_cell(in_file):
    with open(in_file) as f:
        text = f.read()
    m = re.search(
        r'CELL_PARAMETERS[^\n]*\n((?:\s*[-+\d\.E]+\s+[-+\d\.E]+\s+[-+\d\.E]+\s*\n){3})',
        text)
    if not m:
        raise RuntimeError(f"CELL_PARAMETERS not found in {in_file}")
    cell = []
    for line in m.group(1).strip().split('\n'):
        cell.append([float(x) for x in line.split()])
    if len(cell) != 3:
        raise RuntimeError(f"Got {len(cell)} cell rows instead of 3")
    return cell


def parse_last_atomic_positions(out_file):
    with open(out_file) as f:
        text = f.read()
    matches = list(re.finditer(
        r'ATOMIC_POSITIONS\s*\(([^)]+)\)\s*\n((?:[A-Z][a-z]?\s+[-+\d\.E]+\s+[-+\d\.E]+\s+[-+\d\.E]+\s*\n)+)',
        text))
    if not matches:
        raise RuntimeError(f"No ATOMIC_POSITIONS found in {out_file}")
    last = matches[-1]
    units = last.group(1).strip().lower()
    atoms = []
    for line in last.group(2).strip().split('\n'):
        parts = line.split()
        if len(parts) >= 4:
            atoms.append((parts[0], float(parts[1]), float(parts[2]), float(parts[3])))
    return units, atoms, len(matches)


def write_extxyz(cell, units, atoms, out_path):
    a1, a2, a3 = cell
    lat = "{:.8f} {:.8f} {:.8f} {:.8f} {:.8f} {:.8f} {:.8f} {:.8f} {:.8f}".format(
        a1[0], a1[1], a1[2], a2[0], a2[1], a2[2], a3[0], a3[1], a3[2])
    with open(out_path, 'w') as f:
        f.write("{}\n".format(len(atoms)))
        f.write('Lattice="{}" Properties=species:S:1:pos:R:3 pbc="T T T"\n'.format(lat))
        for sym, x, y, z in atoms:
            if units.startswith('crystal'):
                cx = x * a1[0] + y * a2[0] + z * a3[0]
                cy = x * a1[1] + y * a2[1] + z * a3[1]
                cz = x * a1[2] + y * a2[2] + z * a3[2]
            else:  # already angstrom (or alat — would need scale factor)
                cx, cy, cz = x, y, z
            f.write("{:<3s} {:15.10f} {:15.10f} {:15.10f}\n".format(sym, cx, cy, cz))


def main():
    args = sys.argv[1:]
    in_file = args[0] if len(args) >= 1 else "relax.in"
    out_file = args[1] if len(args) >= 2 else "relax.out"
    xyz_path = args[2] if len(args) >= 3 else "v0_relaxed.xyz"

    cell = parse_cell(in_file)
    units, atoms, n_blocks = parse_last_atomic_positions(out_file)

    print("Cell from {}:".format(in_file))
    for row in cell:
        print("  {:.8f} {:.8f} {:.8f}".format(*row))
    print("Found {} ATOMIC_POSITIONS blocks in {}".format(n_blocks, out_file))
    print("Last block units: {}".format(units))
    print("N atoms: {}".format(len(atoms)))

    # composition
    comp = {}
    for sym, *_ in atoms:
        comp[sym] = comp.get(sym, 0) + 1
    print("Composition: {}".format(comp))

    write_extxyz(cell, units, atoms, xyz_path)
    print("Saved: {}".format(Path(xyz_path).resolve()))


if __name__ == "__main__":
    main()
