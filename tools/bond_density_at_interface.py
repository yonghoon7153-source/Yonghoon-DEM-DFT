"""bond_density_at_interface.py — geometric descriptor (UMA-independent).

For each comp (face A and B), build stacked SE/NCM at the well distance d_min,
count interface contacts within cutoff:
  • Li−O   (cutoff 2.8 Å, Li-O paper density correlate)
  • Cl−O   (cutoff 3.2 Å, anti-correlate per agent report)
  • Br−O   (cutoff 3.4 Å)
  • S−Li_NCM (whether NCM has Li; we don't, but keep var for compat)
  • S−O    (cutoff 3.0 Å, repulsive contact)

Normalize by xy area → density (count / Å²).

Then R(density, paper_aJ) across paper comps (comp1, comp2, comp4_v2).

NO UMA calls — purely ASE distance computation. Robust geometric descriptor.

Output:
  /data/work/v30u_ensemble/bond_density_summary.{json,csv}
"""
import json
from pathlib import Path
import numpy as np
from ase.io import read
from ase.neighborlist import NeighborList

WORK = Path('/data/work/v30u_ensemble')
OUT_JSON = WORK / 'bond_density_summary.json'
OUT_CSV  = WORK / 'bond_density_summary.csv'

COMPS = {
    'comp1':    {'se': 'comp1_slab_v2.xyz',            'ncm': 'ncm_7x7x1_PRESERVED.xyz', 'paper': 194, 'family': 'Li6'},
    'comp2':    {'se': 'comp2_slab_v2.xyz',            'ncm': 'ncm_7x7x1_PRESERVED.xyz', 'paper': 180, 'family': 'Li6'},
    'comp4_v1': {'se': 'comp4_slab_v1_PRESERVED.xyz',  'ncm': 'ncm_5x5x1_PRESERVED.xyz', 'paper': 298, 'family': 'Li5.4'},
    'comp4_v2': {'se': 'comp4_slab_v2_PRESERVED.xyz',  'ncm': 'ncm_5x5x1_PRESERVED.xyz', 'paper': 298, 'family': 'Li5.4'},
    'modelC':   {'se': 'modelC_slab_v2_PRESERVED.xyz', 'ncm': 'ncm_5x5x1_PRESERVED.xyz', 'paper': None, 'family': 'Li5.4'},
}

# d_min per comp (from face-flip results) — Wad-well d in Å
D_WELL = 1.4    # use representative well d for all (most face A/B wells in 1.2-1.6)
VACUUM_TOP = 30.0

CUTOFF = {
    ('Li', 'O'):  2.8,
    ('Cl', 'O'):  3.2,
    ('Br', 'O'):  3.4,
    ('S',  'O'):  3.0,
}


def flip_se_xy(se):
    a = se.copy()
    pos = a.positions.copy()
    pos[:, 2] = pos[:, 2].max() + pos[:, 2].min() - pos[:, 2]
    a.set_positions(pos)
    return a


def stack_interface(se, ncm, gap, shift=(0.0, 0.0)):
    se_a = se.copy(); ncm_a = ncm.copy()
    dx, dy = shift
    shift_cart = dx * ncm_a.cell.array[0] + dy * ncm_a.cell.array[1]
    ncm_a.translate([shift_cart[0], shift_cart[1], 0])
    ncm_a.wrap()
    ncm_a.translate([0, 0, -ncm_a.positions[:, 2].min()])
    se_a.translate([0, 0, ncm_a.positions[:, 2].max() - se_a.positions[:, 2].min() + gap])
    n_ncm = len(ncm_a)
    combined = ncm_a + se_a
    new_cell = se.cell.array.copy()
    z_extent = combined.positions[:, 2].max() - combined.positions[:, 2].min()
    new_cell[2] = [0, 0, z_extent + VACUUM_TOP]
    combined.set_cell(new_cell, scale_atoms=False)
    combined.set_pbc([True, True, True])
    return combined, n_ncm


def xy_area(cell):
    a1 = cell[0]; a2 = cell[1]
    return float(np.linalg.norm(np.cross(np.append(a1[:2], 0), np.append(a2[:2], 0))))


def count_contacts(atoms, n_ncm):
    """For atoms in stacked interface (NCM first n_ncm, then SE), count contacts
    between SE atoms and NCM-O atoms by element-pair within element cutoff."""
    pos = atoms.get_positions()
    sym = atoms.get_chemical_symbols()
    is_ncm = np.array([i < n_ncm for i in range(len(atoms))])

    ncm_O = [i for i in range(n_ncm) if sym[i] == 'O']
    if not ncm_O:
        return {}

    cell = atoms.cell.array
    pbc = atoms.pbc

    counts = {f"{el}-O": 0 for el in ['Li', 'Cl', 'Br', 'S']}
    pair_atoms = {f"{el}-O": [] for el in ['Li', 'Cl', 'Br', 'S']}

    # iterate SE atoms × NCM-O atoms with min-image distance
    for i in range(n_ncm, len(atoms)):
        el_se = sym[i]
        if (el_se, 'O') not in CUTOFF: continue
        cutoff = CUTOFF[(el_se, 'O')]
        for j in ncm_O:
            d = atoms.get_distance(i, j, mic=True)
            if d <= cutoff:
                key = f"{el_se}-O"
                counts[key] = counts[key] + 1
                pair_atoms[key].append((i, j, float(d)))

    return counts


def analyze_comp(c, info, face='A'):
    se = read(WORK / info['se'])
    ncm = read(WORK / info['ncm'])
    if face == 'B':
        se = flip_se_xy(se)

    # Build stack at well distance
    stacked, n_ncm = stack_interface(se, ncm, D_WELL, shift=(0, 0))
    A = xy_area(stacked.cell.array)

    counts = count_contacts(stacked, n_ncm)

    # densities
    dens = {k: v / A for k, v in counts.items()}

    return {
        'comp':    c,
        'face':    face,
        'A_A2':    A,
        'n_ncm':   n_ncm,
        'n_se':    len(stacked) - n_ncm,
        'counts':  counts,
        'density_per_A2': dens,
        'paper_aJ': info['paper'],
        'family':   info['family'],
    }


def main():
    rows = []
    for c, info in COMPS.items():
        for face in ['A', 'B']:
            print(f"\n[{c} face {face}]")
            try:
                r = analyze_comp(c, info, face)
                rows.append(r)
                print(f"  area = {r['A_A2']:.1f} Å²,  contacts at d={D_WELL}:")
                for k, n in r['counts'].items():
                    d = r['density_per_A2'][k]
                    print(f"    {k}: {n} contacts  ({d*100:.3f} per 100 Å²)")
            except Exception as e:
                print(f"  FAIL: {e}")

    # ─── R against paper for each bond type ──────────────────────
    print("\n" + "─" * 70)
    print("R(density, paper_aJ) per bond type, per face:")
    print("─" * 70)
    for face in ['A', 'B']:
        rows_face = [r for r in rows if r['face'] == face and r['paper_aJ'] is not None]
        if len(rows_face) < 2:
            continue
        paper = [r['paper_aJ'] for r in rows_face]
        names = [r['comp'] for r in rows_face]
        print(f"\n  face {face}:  comps = {names}, paper = {paper}")
        for bond_type in ['Li-O', 'Cl-O', 'Br-O', 'S-O']:
            dens = [r['density_per_A2'][bond_type] for r in rows_face]
            if np.std(dens) < 1e-9:
                R = np.nan
            else:
                R = float(np.corrcoef(dens, paper)[0, 1])
            print(f"    {bond_type:<6} density: {[f'{x:.4f}' for x in dens]}  →  R = {R:+.3f}")

    # ─── Save ────────────────────────────────────────────────
    json.dump(rows, open(OUT_JSON, 'w'), indent=2, default=str)
    with open(OUT_CSV, 'w') as f:
        f.write("comp,face,family,paper_aJ,A_A2,Li_O_count,Li_O_density,"
                "Cl_O_count,Cl_O_density,Br_O_count,Br_O_density,"
                "S_O_count,S_O_density\n")
        for r in rows:
            d = r['density_per_A2']
            c_ = r['counts']
            f.write(f"{r['comp']},{r['face']},{r['family']},{r['paper_aJ']},{r['A_A2']:.2f},"
                    f"{c_['Li-O']},{d['Li-O']:.5f},"
                    f"{c_['Cl-O']},{d['Cl-O']:.5f},"
                    f"{c_['Br-O']},{d['Br-O']:.5f},"
                    f"{c_['S-O']},{d['S-O']:.5f}\n")
    print(f"\nSaved: {OUT_JSON}")
    print(f"Saved: {OUT_CSV}")


if __name__ == "__main__":
    main()
