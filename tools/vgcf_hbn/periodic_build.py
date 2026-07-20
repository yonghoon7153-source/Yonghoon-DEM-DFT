#!/usr/bin/env python3
"""periodic_build.py — QE periodic-slab models: h-BN coating on VGCF (Li anode).

PIVOT (2026-07-20, user choice): ORCA cluster -> QE periodic slab. No H-edge
artifact, true infinite surface, literature 'minimum unit' = small supercell with
one diluted Li. Builds NxN honeycomb slabs + Li adsorption, vacuum in z, QE-ready.

⚠ PARAMS BELOW ARE PLACEHOLDER pending the 2 litdb digests (Liu 2022 +
h-BN-interfacial-DFT) which pin the papers' exact supercell N, lattice a,
functional/vdW, vacuum, k-points, and E_ads reference. Re-run with confirmed vals.

Cases (per pptx):
  graphene_NxN     VGCF surface
  hbn_NxN          h-BN coating surface
  bilayer_NxN      h-BN on VGCF (common lattice, AB), d0
  Li_on_graphene / Li_on_hbn / Li_in_gallery   adsorption (hollow site)
Emits QE CELL_PARAMETERS + ATOMIC_POSITIONS blocks (+ xyz for viewing).
"""
import numpy as np

A_GR = 2.46    # graphene a (A)   -- placeholder
A_BN = 2.50    # h-BN a (A)       -- placeholder
D0 = 3.33      # interlayer (A)
VAC = 20.0     # vacuum (A)
LI_H = 1.80    # Li height above surface (A)
N = 4          # supercell NxN    -- placeholder (min-unit pending digest)


def sheet(a, N, elemAB, z=0.0):
    a1 = np.array([a, 0.0]); a2 = np.array([a / 2, a * np.sqrt(3) / 2])
    basis = [(np.zeros(2), elemAB[0]), ((a1 + a2) / 3, elemAB[1])]
    coords, elems = [], []
    for i in range(N):
        for j in range(N):
            for b, e in basis:
                p = i * a1 + j * a2 + b
                coords.append([p[0], p[1], z]); elems.append(e)
    cell = np.array([N * a1, N * a2])
    return np.array(coords), elems, cell


def hollow_xy(coords, cell):
    """Ring-center nearest the in-plane cell centre (average of 6 nearest atoms)."""
    c = 0.5 * (cell[0] + cell[1])
    d = np.linalg.norm(coords[:, :2] - c, axis=1)
    six = coords[np.argsort(d)[:6], :2]
    return six.mean(0)


def qe_blocks(coords, elems, cell, name):
    a1, a2 = cell
    z0 = coords[:, 2].min()
    thick = np.ptp(coords[:, 2]) if len(coords) else 0.0
    out = [f"# {name}", "CELL_PARAMETERS angstrom",
           f"  {a1[0]:12.6f} {a1[1]:12.6f}   0.000000",
           f"  {a2[0]:12.6f} {a2[1]:12.6f}   0.000000",
           f"   0.000000   0.000000  {thick + VAC:12.6f}",
           "ATOMIC_POSITIONS angstrom"]
    for e, p in zip(elems, coords):   # slab centred in the vacuum box
        out.append(f"  {e:2s} {p[0]:14.8f} {p[1]:14.8f} {p[2] - z0 + VAC / 2:14.8f}")
    return "\n".join(out) + "\n"


def write_xyz(path, coords, elems, comment=""):
    with open(path, "w") as f:
        f.write(f"{len(coords)}\n{comment}\n")
        for e, p in zip(elems, coords):
            f.write(f"{e:2s} {p[0]:14.8f} {p[1]:14.8f} {p[2]:14.8f}\n")


def main():
    import os
    out = os.path.dirname(os.path.abspath(__file__)) + "/periodic"
    os.makedirs(out, exist_ok=True)

    gC, gE, gcell = sheet(A_GR, N, ("C", "C"))
    bC, bE, bcell = sheet(A_BN, N, ("B", "N"))
    # bilayer: common lattice = graphene a (strain h-BN to match; note in report)
    b2C, b2E, _ = sheet(A_GR, N, ("B", "N"), z=D0)
    biC = np.vstack([gC, b2C]); biE = gE + b2E

    li = lambda xy, z: np.array([[xy[0], xy[1], z]])
    gh = hollow_xy(gC, gcell); bh = hollow_xy(bC, bcell)
    cases = {
        "graphene": (gC, gE, gcell),
        "hbn": (bC, bE, bcell),
        "bilayer": (biC, biE, gcell),
        "Li_on_graphene": (np.vstack([gC, li(gh, LI_H)]), gE + ["Li"], gcell),
        "Li_on_hbn": (np.vstack([bC, li(bh, LI_H)]), bE + ["Li"], bcell),
        "Li_in_gallery": (np.vstack([gC, b2C, li(gh, D0 / 2)]), gE + b2E + ["Li"], gcell),
    }
    print(f"periodic slabs (N={N}, a_gr={A_GR}, a_bn={A_BN}, vac={VAC}A) [PLACEHOLDER params]:")
    for nm, (C, E, cell) in cases.items():
        open(f"{out}/{nm}.qe", "w").write(qe_blocks(C, E, cell, nm))
        write_xyz(f"{out}/{nm}.xyz", C, E, nm)
        from collections import Counter
        d = np.linalg.norm(C[:, None] - C[None], axis=-1); np.fill_diagonal(d, 9)
        print(f"  {nm:16s} {dict(Counter(E))}  n={len(C):3d}  min_d={d.min():.3f}A")
    area = np.linalg.norm(np.cross(np.append(gcell[0], 0), np.append(gcell[1], 0)))
    print(f"  Li-Li image dist (N={N}) ~ {N*A_GR:.2f} A ; cell area {area:.1f} A^2")
    print(f"-> {out}/  (.qe blocks + .xyz). Wrap in full QE input once digest pins ecut/k/func.")


if __name__ == "__main__":
    main()
