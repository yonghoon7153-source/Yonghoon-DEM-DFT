"""Inspect comp4 v2 V0 structure — diagnose why binding curve is anomalous.

Reads xyz file, analyzes:
  1. Composition (atom counts per species — verify Li27 P5 S22 Cl4 Br4)
  2. Z-distribution per species (halogen surface exposure, Li layering)
  3. Slab top/bottom surface composition (which atoms are at z extremes)
  4. Cl, Br positions relative to S framework (PS4 vs free anion sites)
  5. Suspect signs: Cl exposed at surface, Li clustered, abnormal cell shape

Usage:
    python inspect_comp4_v2_v0.py path/to/comp4_v2_V0.xyz
    # OR cif:
    python inspect_comp4_v2_v0.py path/to/comp4_v2.cif

Optional: provide comp4_v1 file as 2nd arg for direct comparison
    python inspect_comp4_v2_v0.py comp4_v2_V0.xyz comp4_v1_post_relax.xyz
"""
import sys
from pathlib import Path
import numpy as np
from ase.io import read

if len(sys.argv) < 2:
    print(__doc__); sys.exit(1)

PATH_V2 = Path(sys.argv[1])
PATH_V1 = Path(sys.argv[2]) if len(sys.argv) > 2 else None


def analyze(atoms, label=""):
    print(f"\n{'='*70}")
    print(f"  {label}: {len(atoms)} atoms")
    print(f"  cell: a={atoms.cell.lengths()[0]:.3f}  b={atoms.cell.lengths()[1]:.3f}  c={atoms.cell.lengths()[2]:.3f}")
    print(f"  angles: α={atoms.cell.angles()[0]:.2f}  β={atoms.cell.angles()[1]:.2f}  γ={atoms.cell.angles()[2]:.2f}")
    vol = atoms.cell.volume
    print(f"  volume: {vol:.2f} Å³  ({vol/len(atoms):.3f} Å³/atom)")
    print(f"{'='*70}")

    sym = atoms.get_chemical_symbols()
    pos = atoms.positions
    z = pos[:, 2]
    z_range = (z.min(), z.max(), z.max() - z.min())
    print(f"\nz range: [{z_range[0]:.3f}, {z_range[1]:.3f}]  (Δz = {z_range[2]:.3f} Å)")

    # Composition
    print(f"\n── Composition ──")
    from collections import Counter
    counts = Counter(sym)
    expected_comp4 = {'Li': 27, 'P': 5, 'S': 22, 'Cl': 4, 'Br': 4}
    for el in ['Li', 'P', 'S', 'Cl', 'Br']:
        n = counts.get(el, 0)
        exp = expected_comp4.get(el, 0)
        flag = "✓" if n == exp else f"⚠ (expected {exp})"
        print(f"  {el}: {n}  {flag}")

    # Per-species z distribution
    print(f"\n── Z distribution per species (relative to slab) ──")
    print(f"  {'species':<8} {'count':>5} {'z_min':>8} {'z_max':>8} {'z_mean':>8} {'z_std':>8}")
    for el in ['Li', 'P', 'S', 'Cl', 'Br']:
        idx = [i for i, s in enumerate(sym) if s == el]
        if not idx:
            continue
        zs = z[idx]
        print(f"  {el:<8} {len(idx):>5d} {zs.min():>+8.3f} {zs.max():>+8.3f} "
              f"{zs.mean():>+8.3f} {zs.std():>8.3f}")

    # Top/bottom 10% surface composition
    z_lo_cut = z.min() + 0.1 * z_range[2]
    z_hi_cut = z.max() - 0.1 * z_range[2]
    bottom_idx = np.where(z <= z_lo_cut)[0]
    top_idx = np.where(z >= z_hi_cut)[0]
    print(f"\n── Surface composition (top/bottom 10% of slab thickness) ──")
    print(f"  Bottom (z ≤ {z_lo_cut:.2f}, n={len(bottom_idx)}):")
    bsym = Counter(sym[i] for i in bottom_idx)
    for el, n in sorted(bsym.items()):
        print(f"    {el}: {n}")
    print(f"  Top (z ≥ {z_hi_cut:.2f}, n={len(top_idx)}):")
    tsym = Counter(sym[i] for i in top_idx)
    for el, n in sorted(tsym.items()):
        print(f"    {el}: {n}")

    # Halogen position diagnosis: are Cl/Br at surface or buried?
    print(f"\n── Halogen surface exposure ──")
    z_mid = (z.min() + z.max()) / 2
    for el in ['Cl', 'Br']:
        idx = [i for i, s in enumerate(sym) if s == el]
        if not idx:
            continue
        zs = z[idx]
        # distance from middle
        dist_from_mid = np.abs(zs - z_mid)
        max_dist = z_range[2] / 2
        relative_pos = dist_from_mid / max_dist  # 0 = middle, 1 = surface
        n_surface = sum(relative_pos > 0.7)  # within outer 30% of slab
        print(f"  {el}: {len(idx)} total, {n_surface} in outer 30% of slab thickness")
        for i, ri in zip(idx, relative_pos):
            mark = " ← SURFACE" if ri > 0.7 else ""
            print(f"    {el}{i:3d}: z={z[i]:+.3f}  rel_pos_from_mid={ri:.2f}{mark}")

    # Bond analysis: P-S, Li-S, Li-halogen, Li-Li distances
    print(f"\n── Nearest-neighbor distances (key bonds) ──")
    from ase.neighborlist import neighbor_list
    cutoff = 4.0
    i_arr, j_arr, d_arr = neighbor_list('ijd', atoms, cutoff)
    pairs = {}
    for i, j, d in zip(i_arr, j_arr, d_arr):
        si, sj = sym[i], sym[j]
        if i < j:  # avoid double counting
            key = tuple(sorted([si, sj]))
            pairs.setdefault(key, []).append(d)
    for pair_key in [('P','S'), ('Li','S'), ('Li','Cl'), ('Li','Br'), ('Li','Li')]:
        ds = pairs.get(pair_key, [])
        if not ds:
            continue
        ds = np.array(ds)
        # Filter by typical range
        rng = {'P-S': (1.8,2.5), 'Li-S':(2.0,3.2), 'Li-Cl':(2.0,3.4),
               'Li-Br':(2.0,3.6), 'Li-Li':(1.5,3.5)}
        lo, hi = rng[f"{pair_key[0]}-{pair_key[1]}"]
        ds = ds[(ds >= lo) & (ds <= hi)]
        if len(ds):
            print(f"  {pair_key[0]}-{pair_key[1]}: n={len(ds)}, "
                  f"mean={ds.mean():.3f} Å, min={ds.min():.3f}, max={ds.max():.3f}")


def main():
    if not PATH_V2.exists():
        print(f"ERROR: {PATH_V2} not found")
        sys.exit(1)

    atoms_v2 = read(PATH_V2)
    analyze(atoms_v2, label=f"comp4 v2 V0 ({PATH_V2.name})")

    if PATH_V1 and PATH_V1.exists():
        atoms_v1 = read(PATH_V1)
        analyze(atoms_v1, label=f"comp4 v1 ({PATH_V1.name})")

        # Direct comparison
        print(f"\n{'='*70}")
        print(f"  v2 - v1 KEY DIFFERENCES")
        print(f"{'='*70}")
        sym_v2 = atoms_v2.get_chemical_symbols()
        sym_v1 = atoms_v1.get_chemical_symbols()
        z_v2 = atoms_v2.positions[:, 2]
        z_v1 = atoms_v1.positions[:, 2]

        for el in ['Cl', 'Br']:
            idx_v2 = [i for i, s in enumerate(sym_v2) if s == el]
            idx_v1 = [i for i, s in enumerate(sym_v1) if s == el]
            if not idx_v2 or not idx_v1:
                continue
            zs_v2 = z_v2[idx_v2]
            zs_v1 = z_v1[idx_v1]
            mid_v2 = (z_v2.min() + z_v2.max()) / 2
            mid_v1 = (z_v1.min() + z_v1.max()) / 2
            half_v2 = (z_v2.max() - z_v2.min()) / 2
            half_v1 = (z_v1.max() - z_v1.min()) / 2
            n_surf_v2 = sum(np.abs(zs_v2 - mid_v2) / half_v2 > 0.7)
            n_surf_v1 = sum(np.abs(zs_v1 - mid_v1) / half_v1 > 0.7)
            print(f"  {el} surface (outer 30% slab):  v1 = {n_surf_v1}/{len(idx_v1)},  v2 = {n_surf_v2}/{len(idx_v2)}")


if __name__ == "__main__":
    main()
