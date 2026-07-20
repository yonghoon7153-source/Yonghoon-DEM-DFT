#!/usr/bin/env python3
"""build_structures.py — VGCF(graphene) / h-BN flake + bilayer models for ORCA.

Project: h-BN coating on VGCF, Li-metal anode (double-lithiophobic sandwich, Liu
Adv. Mater. Interfaces 2022). Finite molecular-flake proxy (graphene-structure
approach, standard per the field), ORCA r2SCAN-3c (D4 dispersion for the vdW
bilayer + Li-pi). Builds three substrates and the Li adsorption start-structures:

  graphene_flake.xyz   circumcoronene-class PAH, H-terminated       <- VGCF surface
  hbn_flake.xyz        BN analog (same lattice, B/N bipartite), H-t  <- h-BN coating
  bilayer.xyz          h-BN stacked on graphene, ring-over-ring, d0  <- coating interface
  Li_on_graphene.xyz / Li_on_hbn.xyz / Li_in_gallery.xyz            <- adsorption starts

Central ring is at the xy-origin so the central hollow site (least edge-biased) is
the adsorption/diffusion site. Everything is a starting geometry -> ORCA relaxes.
"""
import numpy as np

CC = 1.42     # graphene C-C (A)
BN = 1.45     # h-BN B-N (A)
XH = {"C": 1.09, "B": 1.19, "N": 1.01}
D0 = 3.33     # graphene/h-BN interlayer (A), vdW
GALLERY = 3.70  # expanded interlayer to host Li in the sandwich (relaxes in ORCA)
LI_H = 1.85   # initial Li height above a surface (A)


def honeycomb(bond, R):
    """Carbons of a honeycomb disk of radius R, a ring-center at the origin.
    Ring centers on a triangular lattice; carbons = the 6 hexagon vertices."""
    a = bond * np.sqrt(3.0)
    t1 = np.array([a, 0.0]); t2 = np.array([a / 2, a * np.sqrt(3) / 2])
    verts = bond * np.array([[np.cos(np.deg2rad(30 + 60 * k)),
                              np.sin(np.deg2rad(30 + 60 * k))] for k in range(6)])
    seen = {}
    M = 12
    for m in range(-M, M + 1):
        for n in range(-M, M + 1):
            c = m * t1 + n * t2
            for v in verts:
                p = c + v
                key = (round(p[0], 3), round(p[1], 3))
                seen[key] = p
    P = np.array(list(seen.values()))
    P = P[np.linalg.norm(P, axis=1) < R]
    return P


def adjacency(P, cut):
    n = len(P); adj = [[] for _ in range(n)]
    for i in range(n):
        d = np.linalg.norm(P - P[i], axis=1)
        for j in np.where((d > 0.1) & (d < cut))[0]:
            adj[i].append(int(j))
    return adj


def clean_dangling(P, bond):
    """Iteratively drop atoms with <2 in-flake neighbors (bad edge)."""
    while True:
        adj = adjacency(P, bond * 1.25)
        keep = [i for i in range(len(P)) if len(adj[i]) >= 2]
        if len(keep) == len(P):
            return P
        P = P[keep]


def bipartite_2color(adj):
    color = {}
    for s in range(len(adj)):
        if s in color:
            continue
        color[s] = 0; stack = [s]
        while stack:
            u = stack.pop()
            for v in adj[u]:
                if v not in color:
                    color[v] = 1 - color[u]; stack.append(v)
                elif color[v] == color[u]:
                    raise RuntimeError("not bipartite (defect ring)")
    return [color[i] for i in range(len(adj))]


def terminate(P3, elems, bond):
    """Add one H outward on every edge atom (exactly 2 in-flake neighbors)."""
    adj = adjacency(P3[:, :2], bond * 1.25)
    Hs = []
    for i, nb in enumerate(adj):
        if len(nb) >= 3:
            continue
        v = np.zeros(2)
        for j in nb:
            u = P3[i, :2] - P3[j, :2]
            v += u / np.linalg.norm(u)
        v = v / np.linalg.norm(v)
        h = P3[i].copy()
        h[:2] = P3[i, :2] + v * XH[elems[i]]
        Hs.append(h)
    return np.array(Hs) if Hs else np.zeros((0, 3))


def graphene(R=6.5, z=0.0):   # R=6.5 -> C54H18 circumcoronene; R=8.0 -> C84 (size-conv check)
    P = clean_dangling(honeycomb(CC, R), CC)
    P3 = np.c_[P, np.full(len(P), z)]
    elems = ["C"] * len(P3)
    H = terminate(P3, elems, CC)
    return (np.vstack([P3, H]), elems + ["H"] * len(H))


def hbn(R=6.5, z=0.0):        # matches graphene R -> B27N27H18
    P = clean_dangling(honeycomb(BN, R * BN / CC), BN)
    adj = adjacency(P, BN * 1.25)
    col = bipartite_2color(adj)
    elems = ["B" if c == 0 else "N" for c in col]
    P3 = np.c_[P, np.full(len(P), z)]
    H = terminate(P3, elems, BN)
    # H element label follows the edge atom it caps
    Helem = []
    for h in H:
        i = int(np.argmin(np.linalg.norm(P3[:, :2] - h[:2], axis=1)))
        Helem.append("H")
    return (np.vstack([P3, H]), elems + Helem)


def write_xyz(path, coords, elems, comment=""):
    with open(path, "w") as f:
        f.write(f"{len(coords)}\n{comment}\n")
        for e, p in zip(elems, coords):
            f.write(f"{e:2s} {p[0]:14.8f} {p[1]:14.8f} {p[2]:14.8f}\n")


def report(name, coords, elems):
    from collections import Counter
    c = Counter(elems)
    d = np.linalg.norm(coords[:, None, :] - coords[None, :, :], axis=-1)
    np.fill_diagonal(d, 9)
    zspread = np.ptp(coords[:, 2]) if len(coords) else 0
    print(f"  {name:16s} {dict(c)}  natom={len(coords)}  "
          f"min_d={d.min():.3f}A  z_spread={zspread:.3f}A")


def main():
    import os
    out = os.path.dirname(os.path.abspath(__file__)) + "/structures"
    os.makedirs(out, exist_ok=True)

    gC, gE = graphene()
    bC, bE = hbn()
    write_xyz(f"{out}/graphene_flake.xyz", gC, gE, "VGCF proxy: graphene flake (r2SCAN-3c)")
    write_xyz(f"{out}/hbn_flake.xyz", bC, bE, "h-BN coating: BN flake (r2SCAN-3c)")

    # bilayer: h-BN ring-over-ring above graphene, both centered at origin
    bC2 = bC.copy(); bC2[:, 2] += D0
    biC = np.vstack([gC, bC2]); biE = gE + bE
    write_xyz(f"{out}/bilayer.xyz", biC, biE,
              f"h-BN on VGCF(graphene), d0={D0}A ring-over-ring (relax registry+d)")

    # Li adsorption starts (central hollow = origin)
    li = lambda z: np.array([[0.0, 0.0, z]])
    write_xyz(f"{out}/Li_on_graphene.xyz", np.vstack([gC, li(LI_H)]), gE + ["Li"],
              "Li on VGCF(graphene) central hollow")
    write_xyz(f"{out}/Li_on_hbn.xyz", np.vstack([bC, li(LI_H)]), bE + ["Li"],
              "Li on h-BN central hollow")
    gal = bC.copy(); gal[:, 2] += GALLERY
    write_xyz(f"{out}/Li_in_gallery.xyz",
              np.vstack([gC, gal, li(GALLERY / 2)]), gE + bE + ["Li"],
              f"Li in VGCF|h-BN gallery d={GALLERY}A (relaxes)")

    print("built (validation):")
    for n, C, E in [("graphene_flake", gC, gE), ("hbn_flake", bC, bE),
                    ("bilayer", biC, biE)]:
        report(n, C, E)
    print(f"\n-> {out}/  (6 xyz). Next: ORCA r2SCAN-3c inputs (opt) for E_ads/NEB.")


if __name__ == "__main__":
    main()
