"""bond_density_at_interface_full.py — extended interface contact analysis.

For each comp (face A and B), build stacked SE/NCM at d_well, count ALL
SE×NCM-element contacts within cutoff.

NCM atoms: Li_NCM, Ni, Co, Mn, O
SE  atoms: Li_SE, P, S, Cl, Br

Contact pairs analyzed (cutoffs in Å, ionic-radii based + buffer):
  Li-O    2.8    (SE Li - NCM O — main attraction)
  Li-M    3.0    (SE Li - NCM Ni/Co/Mn — cation-cation, mostly repulsive)
  Li-Li   3.0    (SE Li - NCM Li)
  S-O     3.0    (anion-anion contact, repulsive)
  S-M     3.0    (SE S - NCM M — ionic, attractive)
  S-Li    3.0    (SE S - NCM Li — ionic; agent report = family classifier R=-0.90)
  Cl-O    3.2    (anion-anion, repulsive)
  Cl-M    3.3    (anion-cation, attractive)
  Cl-Li   3.2
  Br-O    3.4
  Br-M    3.5
  Br-Li   3.4
  P-O     3.5    (PS4 P approaching NCM O)
  P-M     3.5    (PS4 P approaching NCM M)

For each pair, compute density (count/Å²) and R(density, paper_aJ).
"""
import json
from pathlib import Path
import numpy as np
from ase.io import read

WORK = Path('/data/work/v30u_ensemble')
OUT_JSON = WORK / 'bond_density_full_summary.json'
OUT_CSV  = WORK / 'bond_density_full_summary.csv'

COMPS = {
    'comp1':    {'se': 'comp1_slab_v2.xyz',            'ncm': 'ncm_7x7x1_PRESERVED.xyz', 'paper': 194, 'family': 'Li6'},
    'comp2':    {'se': 'comp2_slab_v2.xyz',            'ncm': 'ncm_7x7x1_PRESERVED.xyz', 'paper': 180, 'family': 'Li6'},
    'comp4_v1': {'se': 'comp4_slab_v1_PRESERVED.xyz',  'ncm': 'ncm_5x5x1_PRESERVED.xyz', 'paper': 298, 'family': 'Li5.4'},
    'comp4_v2': {'se': 'comp4_slab_v2_PRESERVED.xyz',  'ncm': 'ncm_5x5x1_PRESERVED.xyz', 'paper': 298, 'family': 'Li5.4'},
    'modelC':   {'se': 'modelC_slab_v2_PRESERVED.xyz', 'ncm': 'ncm_5x5x1_PRESERVED.xyz', 'paper': None, 'family': 'Li5.4'},
}
D_WELL = 1.4
VACUUM_TOP = 30.0

NCM_M = {'Ni', 'Co', 'Mn'}
NCM_ELEMS = {'Li', 'Ni', 'Co', 'Mn', 'O'}
SE_ELEMS  = {'Li', 'P', 'S', 'Cl', 'Br'}

# Pair cutoffs (SE_element, NCM_element) — Å
# 'Ni' is a token meaning "any of Ni, Co, Mn"
CUTOFFS = {
    ('Li', 'O'):  2.8,
    ('Li', 'Ni'):  3.0,
    ('Li', 'Li'): 3.0,
    ('S',  'O'):  3.0,
    ('S',  'Ni'):  3.0,
    ('S',  'Li'): 3.0,
    ('Cl', 'O'):  3.2,
    ('Cl', 'Ni'):  3.3,
    ('Cl', 'Li'): 3.2,
    ('Br', 'O'):  3.4,
    ('Br', 'Ni'):  3.5,
    ('Br', 'Li'): 3.4,
    ('P',  'O'):  3.5,
    ('P',  'Ni'):  3.5,
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


def count_all_pairs(atoms, n_ncm):
    """Returns dict of {pair_key: count}."""
    sym = atoms.get_chemical_symbols()

    # group NCM atoms by element type → list of indices
    ncm_indices_by_el = {'Li': [], 'Ni': [], 'Co': [], 'Mn': [], 'O': []}
    for i in range(n_ncm):
        e = sym[i]
        if e in ncm_indices_by_el:
            ncm_indices_by_el[e].append(i)

    # Combine M = Ni+Co+Mn
    ncm_indices_M = (ncm_indices_by_el['Ni']
                     + ncm_indices_by_el['Co']
                     + ncm_indices_by_el['Mn'])

    # Pair counts
    counts = {f"{se_e}-{ncm_e}": 0 for (se_e, ncm_e) in CUTOFFS.keys()}

    for i in range(n_ncm, len(atoms)):
        se_e = sym[i]
        if se_e not in SE_ELEMS: continue
        for (s_el, n_el), cutoff in CUTOFFS.items():
            if s_el != se_e: continue
            # pick NCM target indices
            if n_el == 'Ni':
                targets = ncm_indices_M
            elif n_el in ncm_indices_by_el:
                targets = ncm_indices_by_el[n_el]
            else:
                continue
            for j in targets:
                d = atoms.get_distance(i, j, mic=True)
                if d <= cutoff:
                    counts[f"{s_el}-{n_el}"] += 1
    return counts


def analyze_comp(c, info, face='A'):
    se = read(WORK / info['se'])
    ncm = read(WORK / info['ncm'])
    if face == 'B':
        se = flip_se_xy(se)
    stacked, n_ncm = stack_interface(se, ncm, D_WELL, shift=(0, 0))
    A = xy_area(stacked.cell.array)
    counts = count_all_pairs(stacked, n_ncm)
    dens = {k: v / A for k, v in counts.items()}
    return {
        'comp':     c,
        'face':     face,
        'A_A2':     A,
        'n_ncm':    n_ncm,
        'n_se':     len(stacked) - n_ncm,
        'counts':   counts,
        'density':  dens,
        'paper_aJ': info['paper'],
        'family':   info['family'],
    }


def main():
    rows = []
    for c, info in COMPS.items():
        for face in ['A', 'B']:
            try:
                r = analyze_comp(c, info, face)
                rows.append(r)
                print(f"\n[{c} face {face}]  area={r['A_A2']:.1f}, family={r['family']}")
                for k, n in r['counts'].items():
                    d = r['density'][k]
                    if n > 0:
                        print(f"   {k:<8}  count={n:>3}   density={d*100:.3f} /100Å²")
            except Exception as e:
                print(f"  [{c} {face}] FAIL: {e}")

    # ─── R per pair per face ─────────────────────────────────────
    print("\n" + "═" * 90)
    print("R(density, paper_aJ) — per face:")
    print("═" * 90)
    bond_keys = list(CUTOFFS.keys())
    for face in ['A', 'B']:
        rows_face = [r for r in rows if r['face'] == face and r['paper_aJ'] is not None]
        if len(rows_face) < 3:
            continue
        paper = [r['paper_aJ'] for r in rows_face]
        names = [r['comp']    for r in rows_face]
        print(f"\nface {face}:  comps = {names}, paper = {paper}")
        print(f"  {'pair':<8} {'comp1':>9} {'comp2':>9} {'comp4_v1':>9} {'comp4_v2':>9}   {'R':>7}")
        Rs = {}
        for s_el, n_el in bond_keys:
            key = f"{s_el}-{n_el}"
            dens = [r['density'][key] for r in rows_face]
            if np.std(dens) < 1e-9:
                R = np.nan
            else:
                R = float(np.corrcoef(dens, paper)[0, 1])
            Rs[key] = R
            dens_str = "  ".join([f"{x:8.4f}" for x in dens])
            print(f"  {key:<8} {dens_str}   {R:+.3f}")

        # Sort by |R| descending
        sorted_R = sorted([(k, v) for k, v in Rs.items() if not np.isnan(v)],
                          key=lambda x: -abs(x[1]))
        print(f"\n  Strongest correlations (|R| desc, face {face}):")
        for k, R in sorted_R[:8]:
            sign = "✓ paper-matching" if R > 0.7 else ("✗ anti-paper" if R < -0.7 else "")
            print(f"    {k:<8}  R = {R:+.3f}  {sign}")

    # Save
    json.dump(rows, open(OUT_JSON, 'w'), indent=2, default=str)
    with open(OUT_CSV, 'w') as f:
        keys = ['comp', 'face', 'family', 'paper_aJ', 'A_A2']
        for s, n in bond_keys:
            keys.append(f"{s}-{n}_count")
            keys.append(f"{s}-{n}_density")
        f.write(",".join(keys) + "\n")
        for r in rows:
            row = [r['comp'], r['face'], r['family'], str(r['paper_aJ']), f"{r['A_A2']:.2f}"]
            for s, n in bond_keys:
                k = f"{s}-{n}"
                row.append(str(r['counts'][k]))
                row.append(f"{r['density'][k]:.5f}")
            f.write(",".join(row) + "\n")

    print(f"\nSaved: {OUT_JSON}")
    print(f"Saved: {OUT_CSV}")


if __name__ == "__main__":
    main()
