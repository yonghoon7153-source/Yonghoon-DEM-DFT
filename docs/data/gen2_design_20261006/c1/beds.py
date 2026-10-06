#!/usr/bin/env python3
"""designC1 — load the two committed production DEM beds (raw LIGGGHTS dumps) into the
network_conductivity input format, without touching tracked files.

  real_14 : docs/data/real14_reference_20260928/{atom,contact}_2060000.liggghts.gz
            types 1 AM_P (6 um) · 2 AM_S (2 um) · 3 SE (0.5 um) · box 0.05 · plate z 0.0302845 (mesh)
  case15  : docs/data/case15_corner_20261001/{atom,contact}_v4_1710000.liggghts.gz
            types 1 AM_P (6 um) · 2 SE (0.5 um) · box 0.1 · plate z 0.0191455 (mesh)

contact columns = parse_liggghts.parse_contact_file map: c_cpl[7,8] id1,id2 · c_cpl[22] contact_area
(LIGGGHTS geometric intersection disc) · c_cpl[23] delta.
"""
import gzip
import os
import sys

REPO = '/home/user/Yonghoon-DEM-DFT'
HERE = os.path.dirname(os.path.abspath(__file__))
LIB = os.path.join(HERE, 'lib')          # HEAD snapshot of the modules (read-only copies)

BEDS = {
    'real14': dict(atom=f'{REPO}/docs/data/real14_reference_20260928/atom_2060000.liggghts.gz',
                   contact=f'{REPO}/docs/data/real14_reference_20260928/contact_2060000.liggghts.gz',
                   type_map={1: 'AM_P', 2: 'AM_S', 3: 'SE'}, plate_z=0.0302845, box=0.05),
    'case15': dict(atom=f'{REPO}/docs/data/case15_corner_20261001/atom_v4_1710000.liggghts.gz',
                   contact=f'{REPO}/docs/data/case15_corner_20261001/contact_v4_1710000.liggghts.gz',
                   type_map={1: 'AM_P', 2: 'SE'}, plate_z=0.0191455, box=0.1),
}


def _items(path, tag):
    with gzip.open(path, 'rt') as fh:
        lines = fh.read().splitlines()
    for i, ln in enumerate(lines):
        if ln.startswith(tag):
            head = ln.replace(tag, '').split()
            rows = [l.split() for l in lines[i + 1:] if l and not l.startswith('ITEM')]
            return head, rows
    raise ValueError(path)


def load(name):
    b = BEDS[name]
    ha, ra = _items(b['atom'], 'ITEM: ATOMS')
    ia = {k: ha.index(k) for k in ('id', 'type', 'x', 'y', 'z', 'radius')}
    atoms = {}
    for r in ra:
        atoms[int(r[ia['id']])] = {'type': int(r[ia['type']]), 'x': float(r[ia['x']]), 'y': float(r[ia['y']]),
                                   'z': float(r[ia['z']]), 'radius': float(r[ia['radius']])}
    hc, rc = _items(b['contact'], 'ITEM: ENTRIES')
    j1, j2, jA, jD = (hc.index('c_cpl[7]'), hc.index('c_cpl[8]'), hc.index('c_cpl[22]'), hc.index('c_cpl[23]'))
    contacts = [{'id1': int(float(r[j1])), 'id2': int(float(r[j2])), 'contact_area': float(r[jA]),
                 'delta': float(r[jD])} for r in rc]
    return atoms, contacts, b


def nc_module():
    if LIB not in sys.path:
        sys.path.insert(0, LIB)
    import network_conductivity as nc     # HEAD snapshot dfe26fcd4
    return nc


if __name__ == '__main__':
    for n in BEDS:
        A, C, b = load(n)
        print(n, len(A), len(C))
