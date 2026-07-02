#!/usr/bin/env python3
"""Standalone BVSE (Bond-Valence Site Energy) map + percolation barrier for Li.

No ASE/pymatgen — pure numpy + scipy. Parses a P1 CIF directly. Built for
KISTI where only the base conda (numpy/scipy) is guaranteed.

  BVS(r) = Σ_{X in anions} exp((R0_X - d(r,X)) / b)        (anions = S, Cl, O)
  BVSE(r) = (BVS(r) - 1.0)²    (Li⁺ ideal valence = 1.0)
  Li migration barrier ≈ min E such that {BVSE ≤ E} PERCOLATES (spans a full
  period along some axis), measured above the global BVSE minimum.

Usage:
    python3 bvse_standalone.py b2o3_relaxV0.cif --grid 28 --prefix b2o3
Outputs: <prefix>_bvse_map.npy, <prefix>_bvse_summary.json (+ stdout).
"""
import sys, re, json, argparse, math
import numpy as np
from scipy import ndimage

BV = {  # Li–X bond-valence params (Brown-Altermatt), b=0.37
    "S":  (2.105, 0.37),
    "Cl": (2.249, 0.37),
    "O":  (1.466, 0.37),
}
V_IDEAL = 1.0


def parse_cif(fn):
    t = open(fn).read()
    g = lambda k: float(re.search(k + r"\s+([\d.]+)", t).group(1))
    a, b, c = g("_cell_length_a"), g("_cell_length_b"), g("_cell_length_c")
    al, be, ga = (math.radians(g("_cell_angle_" + x)) for x in ("alpha", "beta", "gamma"))
    cs = math.cos
    v = math.sqrt(1 - cs(al)**2 - cs(be)**2 - cs(ga)**2 + 2*cs(al)*cs(be)*cs(ga))
    A = np.array([[a, 0, 0],
                  [b*cs(ga), b*math.sin(ga), 0],
                  [c*cs(be), c*(cs(al)-cs(be)*cs(ga))/math.sin(ga), c*v/math.sin(ga)]])
    # header-aware atom parse: works for both `label symbol x y z` and
    # `symbol label mult x y z occ` column orders (uses the _atom_site_ header).
    sym, frac = [], []
    lines = t.splitlines(); cols = []; inloop = False
    for ln in lines:
        s = ln.strip()
        if s.startswith("_atom_site_"):
            cols.append(s); inloop = True; continue
        if inloop and cols and s and not s.startswith("_") and s != "loop_":
            tok = ln.split()
            if len(tok) < len(cols):
                if frac: break
                continue
            isym = cols.index("_atom_site_type_symbol") if "_atom_site_type_symbol" in cols \
                else cols.index("_atom_site_label")
            ix = cols.index("_atom_site_fract_x"); iy = cols.index("_atom_site_fract_y"); iz = cols.index("_atom_site_fract_z")
            el = "".join(ch for ch in tok[isym] if ch.isalpha())
            sym.append(el); frac.append([float(tok[ix]), float(tok[iy]), float(tok[iz])])
        elif inloop and frac and (s == "" or s.startswith("loop_")):
            break
    return A, np.array(frac), sym


def bvse_map(A, frac, sym, n):
    # anisotropic grid ~uniform Å spacing: n = points along shortest axis
    L = np.linalg.norm(A, axis=1)
    ns = np.maximum(8, np.round(n * L / L.min()).astype(int))
    gx = [np.linspace(0, 1, ns[k], endpoint=False) for k in range(3)]
    GF = np.stack(np.meshgrid(*gx, indexing="ij"), axis=-1)   # (nx,ny,nz,3) fractional
    anA = [(frac[i], BV[s]) for i, s in enumerate(sym) if s in BV]
    bvs = np.zeros(GF.shape[:3])
    for af, (R0, bb) in anA:
        df = GF - af
        df -= np.round(df)                      # minimum image (fractional)
        d = np.linalg.norm(df @ A, axis=-1)      # cartesian distance
        bvs += np.exp((R0 - d) / bb)
    bvse = (bvs - V_IDEAL) ** 2
    return bvse, ns, L


def percolates(mask):
    """True if {mask} spans a full period along any axis (PBC percolation)."""
    for ax in range(3):
        N = mask.shape[ax]
        big = np.concatenate([mask, mask], axis=ax)     # 2x tile along ax
        lbl, nlab = ndimage.label(big)
        if nlab == 0:
            continue
        for k in range(1, nlab + 1):
            idx = np.where(lbl == k)[ax]
            if idx.size and (idx.max() - idx.min()) >= N:   # connects through one period
                return True
    return False


def perc_barrier(bvse, n_levels=60):
    """Min BVSE level (above global min) at which sub-threshold region percolates."""
    lo, hi = float(bvse.min()), float(np.percentile(bvse, 60))
    levels = np.linspace(lo, hi, n_levels)
    for E in levels:
        if percolates(bvse <= E):
            return float(E), float(E - lo)
    return None, None


def li_site_bvs(A, frac, sym):
    anA = [(frac[i], BV[s]) for i, s in enumerate(sym) if s in BV]
    out = []
    for i, s in enumerate(sym):
        if s != "Li":
            continue
        bvs = 0.0
        for af, (R0, bb) in anA:
            df = frac[i] - af; df -= np.round(df)
            d = np.linalg.norm(df @ A)
            bvs += math.exp((R0 - d) / bb)
        out.append(bvs)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cif")
    ap.add_argument("--grid", type=int, default=28, help="points along shortest axis")
    ap.add_argument("--prefix", default="bvse")
    args = ap.parse_args()

    A, frac, sym = parse_cif(args.cif)
    anions = sorted({s for s in sym if s in BV})
    print(f"cif={args.cif}  natoms={len(sym)}  anions={'+'.join(anions)}")
    bvse, ns, L = bvse_map(A, frac, sym, args.grid)
    print(f"cell |a||b||c| = {L[0]:.2f} {L[1]:.2f} {L[2]:.2f} A  grid={tuple(ns)}  ~{L.min()/args.grid:.3f} A/voxel")
    np.save(f"{args.prefix}_bvse_map.npy", bvse)

    Eperc, Ebar = perc_barrier(bvse)
    lis = li_site_bvs(A, frac, sym)
    summary = {
        "cif": args.cif, "n_atoms": len(sym), "anions": anions,
        "grid": [int(x) for x in ns], "voxel_A": round(L.min()/args.grid, 4),
        "bvse_min": round(float(bvse.min()), 5),
        "bvse_perc_level": round(Eperc, 5) if Eperc is not None else None,
        "Li_migration_barrier_BVSE": round(Ebar, 4) if Ebar is not None else None,
        "Li_site_BVS_mean": round(float(np.mean(lis)), 4) if lis else None,
        "Li_site_BVS_std": round(float(np.std(lis)), 4) if lis else None,
        "note": "BVSE barrier = percolation threshold above global min (valence^2 units). "
                "Empirical BVSE; calibrate scale vs comp1/modelc reference run, not absolute eV.",
    }
    json.dump(summary, open(f"{args.prefix}_bvse_summary.json", "w"), indent=2)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
