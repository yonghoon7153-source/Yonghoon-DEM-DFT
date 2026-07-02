#!/usr/bin/env python3
"""Per-atom Voronoi polyhedron volumes -> per-species mean/std = local free-volume
disorder metric (slide 9 style). PBC via 3x3x3 replication + scipy Voronoi/ConvexHull.
numpy+scipy only (no pymatgen). Reads a CIF (triclinic ok).

std(V) = 0  -> crystallographically equivalent sites (ordered).
larger std -> more site disorder (anti-site / dopant local strain).

  python3 tools/comp1_v3/voronoi_volume_disorder.py db/structures/b2o3_relaxV0.cif
"""
import sys, re
import numpy as np
from scipy.spatial import Voronoi, ConvexHull

ELEMS = {"Li","P","S","Cl","B","O","Br","Ni","Nd","Na","Ca","C","N","F","H"}


def cell_matrix(a, b, c, al, be, ga):
    al, be, ga = np.radians([al, be, ga])
    ax = a; bx = b*np.cos(ga); by = b*np.sin(ga)
    cx = c*np.cos(be); cy = c*(np.cos(al)-np.cos(be)*np.cos(ga))/np.sin(ga)
    cz = np.sqrt(max(c*c - cx*cx - cy*cy, 0.0))
    return np.array([[ax,0,0],[bx,by,0],[cx,cy,cz]])


def parse_cif(path):
    P = {}; atoms = []
    for ln in open(path).read().splitlines():
        s = ln.strip()
        for k in ("_cell_length_a","_cell_length_b","_cell_length_c",
                  "_cell_angle_alpha","_cell_angle_beta","_cell_angle_gamma"):
            if s.startswith(k):
                P[k] = float(s.split()[1])
        t = ln.split()
        if len(t) < 4:
            continue
        sym = None
        for tok in t[:2]:
            base = re.sub(r"[0-9]+$", "", tok)
            if base in ELEMS:
                sym = base; break
        if sym is None:
            continue
        nums = [x for x in t if re.match(r"^-?\d+\.\d+", x)]
        if len(nums) < 3:
            continue
        atoms.append((sym, [float(nums[-3]), float(nums[-2]), float(nums[-1])]))
    C = cell_matrix(P["_cell_length_a"], P["_cell_length_b"], P["_cell_length_c"],
                    P["_cell_angle_alpha"], P["_cell_angle_beta"], P["_cell_angle_gamma"])
    syms = [a[0] for a in atoms]
    frac = np.array([a[1] for a in atoms]) % 1.0
    return syms, frac, C


def voronoi_volumes(frac, C):
    N = len(frac)
    shifts = np.array([[i,j,k] for i in (-1,0,1) for j in (-1,0,1) for k in (-1,0,1)])
    pts = np.vstack([(frac + s) @ C for s in shifts])       # 27N; central = (0,0,0) block
    base = np.where((shifts == 0).all(1))[0][0] * N
    vor = Voronoi(pts)
    vols = np.full(N, np.nan)
    for i in range(N):
        reg = vor.regions[vor.point_region[base + i]]
        if len(reg) == 0 or -1 in reg:
            continue
        try:
            vols[i] = ConvexHull(vor.vertices[reg]).volume
        except Exception:
            pass
    return vols


def run(path):
    syms, frac, C = parse_cif(path)
    vols = voronoi_volumes(frac, C)
    sa = np.array(syms)
    Vcell = abs(np.linalg.det(C))
    print(f"\n{path}")
    print(f"  atoms={len(syms)}  cell V={Vcell:.1f} A^3  sum(Voronoi)={np.nansum(vols):.1f} "
          f"(should ~= cell V)  valid={np.sum(~np.isnan(vols))}/{len(syms)}")
    print(f"  {'sp':>3} {'n':>4} {'mean_V':>8} {'std_V':>7}")
    out = {}
    for e in sorted(set(syms)):
        v = vols[sa == e]; v = v[~np.isnan(v)]
        out[e] = (float(v.mean()), float(v.std()), int(len(v)))
        print(f"  {e:>3} {len(v):>4} {v.mean():>8.3f} {v.std():>7.3f}")
    return out


if __name__ == "__main__":
    paths = sys.argv[1:] or ["db/structures/b2o3_relaxV0.cif"]
    for p in paths:
        run(p)
