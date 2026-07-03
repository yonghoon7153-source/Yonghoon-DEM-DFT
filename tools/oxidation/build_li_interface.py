#!/usr/bin/env python3
"""build_li_interface.py — electrolyte | Li-metal interface slab for MLIP-MD.

Builds a coherent (lateral-commensurate) SE|Li slab: reorients the electrolyte so
its a,b lattice vectors lie in the xy-plane, flattens c to an orthogonal slab axis
(vacuum), then fills a Li-metal reservoir (bcc, tiled & cropped to the a,b footprint)
on top with a small initial gap. Bottom SE layers are FixAtoms-frozen to mimic bulk.

Purpose: watch (with UMA MLIP MD, NO DFT) whether Li reduces the SE at the interface
-> P-S bond breaking, Li2S/Li3P (and, for b2o3, metallic LiB) formation. Confirms /
quantifies the *thermodynamic* prediction (b2o3 worse at bare Li metal via LiB) with
actual *dynamics/morphology* that the equilibrium calc could not give.

Runs on kgy (uma env has ASE). Output = interface_<label>_Li.xyz + a geometry report.

  python3 tools/oxidation/build_li_interface.py \
    --electrolyte db/structures/modelc_V0_k663.xyz --label modelc \
    --li_thickness 14 --out interface_modelc_Li.xyz
"""
import argparse
import numpy as np
from ase import Atoms
from ase.io import read, write
from ase.geometry.cell import cellpar_to_cell
from ase.constraints import FixAtoms

A_LI = 3.51            # bcc Li lattice const (A)  -> n_Li = 2/a^3 = 0.0463 /A^3


def reorient_ab_inplane(atoms):
    """Pure rotation to standard orientation: a||x, b in xy-plane (b_z=0), c tilted.
    Structure unchanged (fractional coords preserved)."""
    frac = atoms.get_scaled_positions(wrap=True)
    atoms.set_cell(cellpar_to_cell(atoms.cell.cellpar()), scale_atoms=False)
    atoms.set_scaled_positions(frac)
    return atoms


def fill_li_bcc(a_vec, b_vec, z0, z1):
    """Tile bcc Li over the xy bounding box, keep atoms with a,b-fractional in [0,1)
    and z in [z0,z1). a_vec,b_vec are in the xy-plane after reorientation."""
    a2d = np.array([a_vec[:2], b_vec[:2]])          # rows = a_xy, b_xy
    Minv = np.linalg.inv(a2d.T)                     # cols of a2d.T = a,b
    corners = np.array([[0, 0], a_vec[:2], b_vec[:2], a_vec[:2] + b_vec[:2]])
    (xmin, ymin), (xmax, ymax) = corners.min(0) - A_LI, corners.max(0) + A_LI
    basis = [(0, 0, 0), (0.5, 0.5, 0.5)]
    pos = []
    for i in range(int(np.floor(xmin / A_LI)) - 1, int(np.ceil(xmax / A_LI)) + 2):
        for j in range(int(np.floor(ymin / A_LI)) - 1, int(np.ceil(ymax / A_LI)) + 2):
            for k in range(int(np.floor(z0 / A_LI)) - 1, int(np.ceil(z1 / A_LI)) + 2):
                for bx, by, bz in basis:
                    x, y, z = (i + bx) * A_LI, (j + by) * A_LI, (k + bz) * A_LI
                    if not (z0 <= z < z1):
                        continue
                    f1, f2 = Minv @ np.array([x, y])
                    if 0 <= f1 < 1 and 0 <= f2 < 1:
                        pos.append([x, y, z])
    return np.array(pos)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--electrolyte", required=True)
    ap.add_argument("--label", required=True)
    ap.add_argument("--li_thickness", type=float, default=14.0, help="Li reservoir thickness (A)")
    ap.add_argument("--gap", type=float, default=2.2, help="initial SE-Li gap (A)")
    ap.add_argument("--vac_bottom", type=float, default=2.0)
    ap.add_argument("--vac_top", type=float, default=12.0)
    ap.add_argument("--fix_bottom", type=float, default=6.0, help="freeze SE atoms within this many A of the bottom")
    ap.add_argument("--supercell", type=int, nargs=2, default=[1, 1], help="lateral repeat of SE (a b) before building")
    ap.add_argument("--out", default=None)
    a = ap.parse_args()

    se = read(a.electrolyte)
    if a.supercell != [1, 1]:
        se = se.repeat((a.supercell[0], a.supercell[1], 1))
    se = reorient_ab_inplane(se)
    se.positions[:, 2] += a.vac_bottom - se.positions[:, 2].min()     # sit SE at z=vac_bottom
    zmax = se.positions[:, 2].max()
    a_vec, b_vec = se.cell[0], se.cell[1]

    z0, z1 = zmax + a.gap, zmax + a.gap + a.li_thickness
    li_pos = fill_li_bcc(a_vec, b_vec, z0, z1)
    Ztot = z1 + a.vac_top

    combined = se + Atoms(["Li"] * len(li_pos), positions=li_pos)
    combined.set_cell(np.array([a_vec, b_vec, [0, 0, Ztot]]))
    combined.pbc = [True, True, True]
    zc = combined.positions[:, 2]
    mask = [(i < len(se)) and (zc[i] < a.vac_bottom + a.fix_bottom) for i in range(len(combined))]
    combined.set_constraint(FixAtoms(mask=mask))

    out = a.out or f"interface_{a.label}_Li.xyz"
    write(out, combined)

    area = np.linalg.norm(np.cross(a_vec, b_vec))
    dens = len(li_pos) / (area * a.li_thickness)
    print(f"[{a.label}] SE={len(se)}  Li={len(li_pos)}  total={len(combined)}  fixed_bottom={sum(mask)}")
    print(f"  lateral |a|={np.linalg.norm(a_vec):.3f} |b|={np.linalg.norm(b_vec):.3f}  area={area:.1f} A^2")
    print(f"  SE z-span={zmax - a.vac_bottom:.1f} A | Li {z0:.1f}-{z1:.1f} A (thick {a.li_thickness}) | cell Z={Ztot:.1f}")
    print(f"  Li number density={dens:.4f}/A^3  (bulk bcc target 0.0463; relax/MD will settle it)")
    print(f"  -> {out}   [VESTA it: SE slab at bottom (frozen layer), Li reservoir on top, vacuum above]")
    if abs(dens - 0.0463) / 0.0463 > 0.15:
        print(f"  !! Li density off by >15% from bulk — check li_thickness / cropping.")


if __name__ == "__main__":
    main()
