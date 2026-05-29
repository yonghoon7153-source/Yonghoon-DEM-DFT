#!/usr/bin/env python3
"""Generate QE PBE+U+ISPIN=2 (AFM) relax input from a LiNiO2 slab xyz.

Re-uses settings verified in the Nd-doped V0 DFT relax + adds Choi 2025 /
Wang 2006 conventions for Ni:
- U_Ni = 6.2 eV (ortho-atomic projectors, QE 7.4 HUBBARD card)
- Collinear AFM: Ni1↑ / Ni2↓ assigned by xy checkerboard inside each layer
- starting_magnetization ±0.5
- pot/wfc_extrapolation = 'none' (Nd-debug lesson — prevents negative rho)
- mixing_beta = 0.1, mixing_mode = 'plain', electron_maxstep = 500
- conv_thr = 1e-6, forc_conv_thr = 1e-3 (partial-relax / collapse check)

Freezes bottom N% atoms via if_pos = 0 0 0 (default 50%).

Usage:
    python3 build_linio2_dft_input.py \\
        --xyz <slab_init.xyz> \\
        --out <out_dir>/relax.in \\
        --freeze_fraction 0.5 \\
        --nstep 30 \\
        --prefix linio2_104_slab \\
        --kgrid 2 2 1
"""
import argparse, json
from pathlib import Path
import numpy as np


def detect_layers(z, gap_threshold=0.8):
    """Return layer index for each atom (0=bottom)."""
    order = np.argsort(z)
    z_sorted = z[order]
    layer = np.zeros(len(z), dtype=int)
    cur = 0
    for k in range(1, len(z_sorted)):
        if z_sorted[k] - z_sorted[k - 1] > gap_threshold:
            cur += 1
        layer[order[k]] = cur
    return layer


def assign_afm_checkerboard(ni_xy, layer_idx):
    """Within each layer, assign Ni atoms to spin-up / spin-down by xy
    checkerboard (nearest-neighbor opposite). Returns 0 (spin up = Ni1) or
    1 (spin down = Ni2) per atom."""
    spin = np.zeros(len(ni_xy), dtype=int)
    for lay in np.unique(layer_idx):
        idx = np.where(layer_idx == lay)[0]
        if len(idx) == 0:
            continue
        # sort by (x, y) and alternate
        order = idx[np.lexsort((ni_xy[idx, 1], ni_xy[idx, 0]))]
        spin[order[1::2]] = 1
    return spin


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--xyz", required=True, help="slab xyz (extxyz from build_linio2_slab.py)")
    ap.add_argument("--out", required=True, help="output relax.in path")
    ap.add_argument("--prefix", default="linio2_104_slab")
    ap.add_argument("--pseudo_dir", default="/data/work/pseudo")
    ap.add_argument("--li_pseudo", default="li_pbe_v1.4.uspp.F.UPF")
    ap.add_argument("--ni_pseudo", default="ni_pbe_v1.4.uspp.F.UPF")
    ap.add_argument("--o_pseudo", default="O.pbe-n-kjpaw_psl.0.1.UPF")
    ap.add_argument("--U_Ni", type=float, default=6.2,
                    help="Hubbard U on Ni 3d (eV); Wang 2006 / Choi 2025 standard")
    ap.add_argument("--mag_init", type=float, default=0.5,
                    help="starting_magnetization magnitude per Ni (±)")
    ap.add_argument("--freeze_fraction", type=float, default=0.5,
                    help="fraction of atoms (by z, bottom) to freeze (if_pos=0,0,0)")
    ap.add_argument("--kgrid", type=int, nargs=3, default=[2, 2, 1])
    ap.add_argument("--ecutwfc", type=float, default=60.0)
    ap.add_argument("--ecutrho", type=float, default=480.0)
    ap.add_argument("--conv_thr", type=float, default=1e-6)
    ap.add_argument("--mixing_beta", type=float, default=0.1)
    ap.add_argument("--electron_maxstep", type=int, default=500)
    ap.add_argument("--nstep", type=int, default=30,
                    help="max ionic steps (30 = partial relax / collapse check)")
    ap.add_argument("--forc_conv_thr", type=float, default=1e-3)
    args = ap.parse_args()

    # Read slab
    from ase.io import read
    atoms = read(args.xyz)
    n = len(atoms)
    sym = np.array(atoms.get_chemical_symbols())
    pos = atoms.positions
    cell = atoms.cell.array

    n_li = int((sym == "Li").sum())
    n_ni = int((sym == "Ni").sum())
    n_o = int((sym == "O").sum())
    print(f"Slab: {n} atoms (Li={n_li}, Ni={n_ni}, O={n_o})")
    print(f"Cell:\n{cell}")

    # Freeze bottom fraction by z
    z = pos[:, 2]
    z_cut = np.sort(z)[int(args.freeze_fraction * n) - 1]
    frozen = z <= z_cut
    print(f"Freeze (if_pos=0,0,0): {frozen.sum()}/{n} atoms (z ≤ {z_cut:.2f} Å, "
          f"{frozen.sum()*100/n:.0f}%)")

    # Layer detection + AFM assignment for Ni
    layer = detect_layers(z)
    n_layers = layer.max() + 1
    print(f"Detected {n_layers} atomic layers (gap threshold 0.8 Å)")

    ni_mask = sym == "Ni"
    ni_xy = pos[ni_mask, :2]
    ni_layer = layer[ni_mask]
    ni_spin = assign_afm_checkerboard(ni_xy, ni_layer)  # 0 = Ni1↑, 1 = Ni2↓
    n_ni1 = int((ni_spin == 0).sum())
    n_ni2 = int((ni_spin == 1).sum())
    print(f"AFM split: Ni1↑ = {n_ni1}, Ni2↓ = {n_ni2}")
    if abs(n_ni1 - n_ni2) > 1:
        print(f"  ⚠ unbalanced AFM (diff {abs(n_ni1-n_ni2)}) — net spin ≠ 0")

    # Build atomic_species + atomic_positions with Ni1/Ni2 labels
    out_pos = []
    ni_count = 0
    for i in range(n):
        s = sym[i]
        if s == "Ni":
            label = "Ni1" if ni_spin[ni_count] == 0 else "Ni2"
            ni_count += 1
        else:
            label = s
        ipos = "0 0 0" if frozen[i] else "1 1 1"
        out_pos.append(
            f"  {label:<3} {pos[i,0]:18.12f} {pos[i,1]:18.12f} {pos[i,2]:18.12f}  {ipos}"
        )

    # Build relax.in
    inp = f"""&CONTROL
    calculation     = 'relax'
    prefix          = '{args.prefix}'
    outdir          = './tmp'
    pseudo_dir      = '{args.pseudo_dir}'
    tprnfor         = .true.
    tstress         = .true.
    forc_conv_thr   = {args.forc_conv_thr:.1e}
    etot_conv_thr   = 1.0d-6
    nstep           = {args.nstep}
    disk_io         = 'low'
/
&SYSTEM
    ibrav           = 0
    nat             = {n}
    ntyp            = 4
    ecutwfc         = {args.ecutwfc}
    ecutrho         = {args.ecutrho}
    occupations     = 'smearing'
    smearing        = 'mv'
    degauss         = 0.01
    nspin           = 2
    starting_magnetization(2) = +{args.mag_init}   ! Ni1 up
    starting_magnetization(3) = -{args.mag_init}   ! Ni2 down (AFM)
    nosym           = .true.
/
&ELECTRONS
    conv_thr        = {args.conv_thr:.1e}
    mixing_beta     = {args.mixing_beta}
    mixing_mode     = 'plain'
    mixing_ndim     = 8
    electron_maxstep = {args.electron_maxstep}
    diagonalization = 'david'
/
&IONS
    ion_dynamics      = 'bfgs'
    pot_extrapolation = 'none'   ! Nd-debug lesson: prevents negative rho
    wfc_extrapolation = 'none'
/
&CELL
    cell_dofree = 'none'
/

HUBBARD ortho-atomic
U Ni1-3d {args.U_Ni}
U Ni2-3d {args.U_Ni}

ATOMIC_SPECIES
  Li   6.94  {args.li_pseudo}
  Ni1 58.69  {args.ni_pseudo}
  Ni2 58.69  {args.ni_pseudo}
  O   16.00  {args.o_pseudo}

CELL_PARAMETERS angstrom
  {cell[0,0]:18.12f} {cell[0,1]:18.12f} {cell[0,2]:18.12f}
  {cell[1,0]:18.12f} {cell[1,1]:18.12f} {cell[1,2]:18.12f}
  {cell[2,0]:18.12f} {cell[2,1]:18.12f} {cell[2,2]:18.12f}

ATOMIC_POSITIONS angstrom
""" + "\n".join(out_pos) + f"""

K_POINTS automatic
  {args.kgrid[0]} {args.kgrid[1]} {args.kgrid[2]} 0 0 0
"""

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(inp)
    print(f"\nWrote {out_path}")

    # Sidecar metadata
    meta_path = out_path.parent / f"{out_path.stem}_meta.json"
    json.dump({
        "n_atoms": n,
        "n_Li": n_li, "n_Ni": n_ni, "n_O": n_o,
        "n_Ni1_up": n_ni1, "n_Ni2_down": n_ni2,
        "n_frozen": int(frozen.sum()),
        "freeze_fraction": args.freeze_fraction,
        "U_Ni_eV": args.U_Ni,
        "mag_init": args.mag_init,
        "kgrid": args.kgrid,
        "ecutwfc": args.ecutwfc,
        "ecutrho": args.ecutrho,
        "conv_thr": args.conv_thr,
        "mixing_beta": args.mixing_beta,
        "nstep": args.nstep,
        "forc_conv_thr": args.forc_conv_thr,
        "input_xyz": str(args.xyz),
    }, open(meta_path, "w"), indent=2)
    print(f"Wrote {meta_path}")


if __name__ == "__main__":
    main()
