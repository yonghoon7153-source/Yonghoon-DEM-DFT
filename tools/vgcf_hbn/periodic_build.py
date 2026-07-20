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

# PINNED from digests (Shi 2017 QE/PBE-D2/PAW, k<0.05/A, vac 10-15A; Liu 2022 VASP).
A_GR = 2.46    # graphene a (A)
A_BN = 2.46    # h-BN strained to graphene (-1.6% vs native 2.50) -> common lattice,
               #   so the sandwich and Shi eq5 (E_iface ~ E_bottom + E_hBN) are self-consistent.
D0 = 3.33      # bare bilayer interlayer (A), vdW
VAC = 18.0     # vacuum (A)  (Shi 10-15; 18 safe for sandwich+Li)
LI_H = 1.80    # Li height above surface (A)
GAL = 3.90     # expanded interlayer to host Li in the sandwich (relaxes in QE)
N = 4          # 4x4 supercell -> Li-Li image 9.84 A (min unit; 5x5 = conv check)


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


def hbn_stack(a, N, nlayers, z0=0.0):
    """nlayers of h-BN, AA' stacking (B over N). Shi: 1L adsorption, 2L DOS/tunneling."""
    coords = []; elems = []; cell = None
    for L in range(nlayers):
        ab = ("B", "N") if L % 2 == 0 else ("N", "B")   # AA': B sits over N
        c, e, cell = sheet(a, N, ab, z=z0 + L * D0)
        coords.append(c); elems += e
    return np.vstack(coords), elems, cell


def graphene_stack(a, N, nlayers, z0=0.0):
    """nlayers of graphene, AB (Bernal) stacking — VGCF is multilayer graphite."""
    a1 = np.array([a, 0.0]); a2 = np.array([a / 2, a * np.sqrt(3) / 2])
    shift = (a1 + a2) / 3                                 # AB: one C-C bond per layer
    coords = []; elems = []; cell = None
    for L in range(nlayers):
        c, e, cell = sheet(a, N, ("C", "C"), z=z0 + L * D0)
        c[:, :2] += L * shift
        coords.append(c); elems += e
    return np.vstack(coords), elems, cell


def main():
    import os
    out = os.path.dirname(os.path.abspath(__file__)) + "/periodic"
    os.makedirs(out, exist_ok=True)

    gC, gE, gcell = sheet(A_GR, N, ("C", "C"))
    bC, bE, bcell = sheet(A_BN, N, ("B", "N"))
    # bilayer: bare h-BN on graphene at vdW spacing D0 (interlayer-binding ref)
    b2C, b2E, _ = sheet(A_GR, N, ("B", "N"), z=D0)
    biC = np.vstack([gC, b2C]); biE = gE + b2E
    # gallery: h-BN lifted to GAL so a Li layer fits between (relaxes in QE)
    b3C, _, _ = sheet(A_GR, N, ("B", "N"), z=GAL)

    li = lambda xy, z: np.array([[xy[0], xy[1], z]])
    gh = hollow_xy(gC, gcell); bh = hollow_xy(bC, bcell)
    cases = {
        "graphene": (gC, gE, gcell),
        "hbn": (bC, bE, bcell),
        "bilayer": (biC, biE, gcell),
        "Li_on_graphene": (np.vstack([gC, li(gh, LI_H)]), gE + ["Li"], gcell),
        "Li_on_hbn": (np.vstack([bC, li(bh, LI_H)]), bE + ["Li"], bcell),
        "Li_in_gallery": (np.vstack([gC, b3C, li(gh, GAL / 2)]), gE + b2E + ["Li"], gcell),
    }
    # --- 2-layer h-BN variants (electron-blocking + layer convergence; Shi's 2L) ---
    h2C, h2E, h2cell = hbn_stack(A_BN, N, 2)                     # bare 2L h-BN
    h2h = hollow_xy(h2C, h2cell)
    cg2, ce2, _ = hbn_stack(A_GR, N, 2, z0=D0)                   # 2L h-BN on VGCF
    gl2, ge2, _ = hbn_stack(A_GR, N, 2, z0=GAL)                  # 2L cap over gallery Li
    cases.update({
        "hbn_2L": (h2C, h2E, h2cell),
        "Li_on_hbn_2L": (np.vstack([h2C, li(h2h, D0 + LI_H)]), h2E + ["Li"], h2cell),
        "bilayer_2L": (np.vstack([gC, cg2]), gE + ce2, gcell),
        "Li_in_gallery_2L": (np.vstack([gC, gl2, li(gh, GAL / 2)]), gE + ge2 + ["Li"], gcell),
    })
    # --- 2-layer graphene (VGCF substrate convergence; AB/Bernal, graphite fidelity) ---
    #     GATE: if Li_on_graphene_2L delta(2L-1L) is small, 1L VGCF is validated and the
    #     gallery stays 1L-graphene (no 4-way graphene x h-BN blow-up); else add 2L-gr gallery.
    g2C, g2E, g2cell = graphene_stack(A_GR, N, 2)
    g2top = g2C[g2C[:, 2] > g2C[:, 2].max() - 0.5]          # hollow of the TOP layer (AB shift)
    g2h = hollow_xy(g2top, g2cell)
    cases.update({
        "graphene_2L": (g2C, g2E, g2cell),
        "Li_on_graphene_2L": (np.vstack([g2C, li(g2h, D0 + LI_H)]), g2E + ["Li"], g2cell),
    })
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
