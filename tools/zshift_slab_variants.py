"""Generate z-shifted slab variants for surface termination sampling.

For any comp's slab xyz, this script:
  1. Rolls atoms along z axis by N_SHIFTS fractions (default 5: 0%, 20%, 40%, 60%, 80%)
  2. Wraps back into the periodic cell — exposes different layer at z=0 surface
  3. For each variant, analyzes surface composition + halogen exposure
  4. Saves: slab_zshiftN.xyz + summary CSV

This is the PIPELINE.md z-cut sampling protocol applied uniformly to every
comp (comp1, comp2, comp4, modelC). Pick the variant with surface chemistry
closest to v1 (halogen-poor or Br-only at z=0 surface).

Usage:
    python zshift_slab_variants.py comp4_slab_v2_PRESERVED.xyz \
        --out_dir comp4_v2_zshifts --n_shifts 5

Output:
    comp4_v2_zshifts/comp4_v2_zshift0.xyz  (no shift)
    comp4_v2_zshifts/comp4_v2_zshift1.xyz  (20% c shift)
    ... up to zshift{N-1}.xyz
    comp4_v2_zshifts/zshift_summary.csv    (per-variant surface analysis)
"""
import sys, csv
from pathlib import Path
from collections import Counter
import argparse
import numpy as np
from ase.io import read, write


def analyze_surface(atoms, surface_pct=0.10):
    """Return composition of bottom & top slab surfaces (within surface_pct of slab thickness)."""
    z = atoms.positions[:, 2]
    sym = atoms.get_chemical_symbols()
    z_lo, z_hi = z.min(), z.max()
    dz = z_hi - z_lo
    bot_cut = z_lo + surface_pct * dz
    top_cut = z_hi - surface_pct * dz
    bot_idx = np.where(z <= bot_cut)[0]
    top_idx = np.where(z >= top_cut)[0]
    bot = Counter(sym[i] for i in bot_idx)
    top = Counter(sym[i] for i in top_idx)
    return bot, top, len(bot_idx), len(top_idx)


def halogen_at_surface(atoms, surface_pct=0.10):
    """Count Cl/Br on bottom surface (NCM contact side)."""
    z = atoms.positions[:, 2]
    sym = atoms.get_chemical_symbols()
    z_lo = z.min()
    dz = z.max() - z_lo
    bot_cut = z_lo + surface_pct * dz
    n_cl = sum(1 for i, s in enumerate(sym) if s == 'Cl' and z[i] <= bot_cut)
    n_br = sum(1 for i, s in enumerate(sym) if s == 'Br' and z[i] <= bot_cut)
    return n_cl, n_br


def roll_z(atoms, frac):
    """Roll atoms along z by fraction of c-axis length, wrap into cell."""
    a = atoms.copy()
    cz = a.cell[2, 2]
    if cz <= 0:
        # rhombo cells may have non-orthogonal — use cell.lengths()[2]
        cz = a.cell.lengths()[2]
    shift_z = frac * cz
    pos = a.positions.copy()
    pos[:, 2] = (pos[:, 2] + shift_z) % cz
    a.set_positions(pos)
    return a


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('input_xyz')
    p.add_argument('--out_dir', default=None,
                   help='output directory (default: <input>_zshifts)')
    p.add_argument('--n_shifts', type=int, default=5,
                   help='number of z-shifts (default 5: 0/N, 1/N, ..., (N-1)/N)')
    p.add_argument('--surface_pct', type=float, default=0.10,
                   help='surface region = outer this fraction (default 0.10)')
    args = p.parse_args()

    in_path = Path(args.input_xyz)
    if args.out_dir is None:
        out_dir = in_path.parent / (in_path.stem + "_zshifts")
    else:
        out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    atoms = read(in_path)
    print(f"Loaded {len(atoms)} atoms from {in_path}")
    print(f"Cell c-axis: {atoms.cell.lengths()[2]:.3f} Å, slab z range: "
          f"[{atoms.positions[:,2].min():.2f}, {atoms.positions[:,2].max():.2f}]")
    print(f"Output dir: {out_dir}")

    # Analyze original
    bot0, top0, _, _ = analyze_surface(atoms, args.surface_pct)
    n_cl0, n_br0 = halogen_at_surface(atoms, args.surface_pct)
    print(f"\nOriginal (no shift):")
    print(f"  bottom surface: {dict(bot0)}")
    print(f"  top surface:    {dict(top0)}")
    print(f"  bottom halogens: Cl={n_cl0}, Br={n_br0}")

    # Generate variants
    rows = []
    print(f"\nGenerating {args.n_shifts} z-shift variants:")
    for i in range(args.n_shifts):
        frac = i / args.n_shifts
        a_shifted = roll_z(atoms, frac)
        out_path = out_dir / f"{in_path.stem}_zshift{i}.xyz"
        write(out_path, a_shifted)
        bot, top, n_b, n_t = analyze_surface(a_shifted, args.surface_pct)
        n_cl, n_br = halogen_at_surface(a_shifted, args.surface_pct)
        rows.append({
            'zshift_idx': i, 'frac': f"{frac:.3f}",
            'shift_A': f"{frac * atoms.cell.lengths()[2]:.3f}",
            'bot_Li': bot.get('Li', 0), 'bot_P': bot.get('P', 0),
            'bot_S': bot.get('S', 0), 'bot_Cl': bot.get('Cl', 0),
            'bot_Br': bot.get('Br', 0),
            'top_Li': top.get('Li', 0), 'top_P': top.get('P', 0),
            'top_S': top.get('S', 0), 'top_Cl': top.get('Cl', 0),
            'top_Br': top.get('Br', 0),
            'file': out_path.name,
        })
        flag = ""
        if n_cl == 0 and n_br > 0: flag = " ← v1-like (Br only at surface)"
        if n_cl == 0 and n_br == 0: flag = " ← halogen-free surface (cleanest)"
        if n_cl > 0: flag = f" ⚠ Cl exposed (n={n_cl})"
        print(f"  zshift{i} (frac {frac:.2f}, {frac*atoms.cell.lengths()[2]:.2f} Å): "
              f"bot Cl={n_cl} Br={n_br}{flag}")

    csv_path = out_dir / "zshift_summary.csv"
    with open(csv_path, 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print(f"\nSaved: {csv_path}")
    print(f"\nNext: pick the zshift variant with halogen-poor or Br-only bottom surface,")
    print(f"      then run v30u UMA Z-scan with that xyz as comp slab input.")


if __name__ == '__main__':
    main()
