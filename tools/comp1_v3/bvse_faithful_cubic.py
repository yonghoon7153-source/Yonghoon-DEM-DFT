#!/usr/bin/env python3
"""Faithful-cubic BVSE pipeline: original cell vs conventional-cubic approximant.

For each system (modelc, b2o3, lpsocl):
  1. load the ACTUAL relaxed structure (June sources, no idealization)
  2. BVSE on the original cell (June convention: softBV Li-X, (BVS-1)^2,
     ~0.25 A voxel, channel %% = voxels with map-min <= iso)
  3. build the faithful conventional-cubic approximant: C1=A2+p3-A1,
     C2=A1+p3-A2, C3=A1+A2-p3 with p3=A3/N (fcc primitive stack) and fill
     with periodic images of the REAL atoms (origin chosen by composition
     score; dopants required inside)
  4. BVSE on the cubic cell, same convention
  5. export aboveMin .cube + .vesta scenes + summary json + comparison csv/png
"""
import json, math, os, re
import numpy as np
from scipy import ndimage

BOHR = 0.529177210903
BV = {"S": (2.105, 0.37), "Cl": (2.249, 0.37), "O": (1.466, 0.37)}
ZNUM = {"Li": 3, "B": 5, "O": 8, "P": 15, "S": 16, "Cl": 17}
ISOS = [0.25, 0.5, 1.0, 1.5, 2.0]
OUT = os.path.join(os.getcwd(), "bvse_out")
os.makedirs(OUT, exist_ok=True)
REPO = "/home/user/Yonghoon-DEM-DFT"


# ---------- structure loaders (each returns A[3x3] A-rows, frac Nx3, sym list) ----------
def cell_from_par(a, b, c, al, be, ga):
    al, be, ga = map(math.radians, (al, be, ga))
    cs = math.cos
    v = math.sqrt(1 - cs(al)**2 - cs(be)**2 - cs(ga)**2 + 2*cs(al)*cs(be)*cs(ga))
    return np.array([[a, 0, 0],
                     [b*cs(ga), b*math.sin(ga), 0],
                     [c*cs(be), c*(cs(al)-cs(be)*cs(ga))/math.sin(ga), c*v/math.sin(ga)]])


def load_vesta_struc(fn):
    t = open(fn).read()
    cp = re.search(r"CELLP\n\s*([\d.\- ]+)\n", t).group(1).split()
    A = cell_from_par(*[float(x) for x in cp[:6]])
    sym, frac = [], []
    m = re.search(r"STRUC\n(.*?)\n  0 0 0 0 0 0 0", t, re.S)
    for ln in m.group(1).splitlines():
        p = ln.split()
        if len(p) >= 7 and p[0].isdigit():
            sym.append(p[1]); frac.append([float(p[4]), float(p[5]), float(p[6])])
    return A, np.array(frac), sym


def load_vasp(fn):
    L = open(fn).read().splitlines()
    scale = float(L[1])
    A = np.array([[float(x) for x in L[i].split()] for i in (2, 3, 4)]) * scale
    species = L[5].split(); counts = [int(x) for x in L[6].split()]
    assert L[7].strip().lower().startswith("cart")
    sym, cart = [], []
    k = 8
    for s, n in zip(species, counts):
        for _ in range(n):
            cart.append([float(x) for x in L[k].split()[:3]]); sym.append(s); k += 1
    frac = np.array(cart) @ np.linalg.inv(A)
    return A, frac % 1.0, sym


def load_cube_header(fn):
    L = open(fn).read().splitlines()
    nat = int(L[2].split()[0])
    axes = [L[i].split() for i in (3, 4, 5)]
    ns = [int(ax[0]) for ax in axes]
    A = np.array([[float(x) for x in ax[1:4]] for ax in axes]) * np.array(ns)[:, None] * BOHR
    inv = {v: k for k, v in ZNUM.items()}
    sym, cart = [], []
    for i in range(6, 6 + nat):
        p = L[i].split()
        sym.append(inv[int(p[0])]); cart.append([float(x)*BOHR for x in p[2:5]])
    frac = np.array(cart) @ np.linalg.inv(A)
    return A, frac % 1.0, sym


# ---------- BVSE (June convention) ----------
def bvse_map(A, frac, sym, n=28):
    L = np.linalg.norm(A, axis=1)
    ns = np.maximum(8, np.round(n * L / L.min()).astype(int))
    gx = [np.linspace(0, 1, ns[k], endpoint=False) for k in range(3)]
    GF = np.stack(np.meshgrid(*gx, indexing="ij"), axis=-1)
    bvs = np.zeros(GF.shape[:3])
    for i, s in enumerate(sym):
        if s not in BV:
            continue
        R0, bb = BV[s]
        df = GF - frac[i]
        df -= np.round(df)
        d = np.linalg.norm(df @ A, axis=-1)
        bvs += np.exp((R0 - d) / bb)
    return (bvs - 1.0) ** 2, ns, L


def bvse_map_box(C, org_cart, A, frac, sym, n=40):
    """BVSE of the TRUE A-periodic crystal, sampled on the grid of the cubic
    box C (+origin). No box-PBC physics: distances use A-cell min-image, so
    the map is an exact crop of the real crystal's BVSE in the cubic frame."""
    lens = np.linalg.norm(C, axis=1)
    ns = np.maximum(8, np.round(n * lens / lens.min()).astype(int))
    gx = [np.linspace(0, 1, ns[k], endpoint=False) for k in range(3)]
    GF = np.stack(np.meshgrid(*gx, indexing="ij"), axis=-1)
    R = GF @ C + org_cart
    invA = np.linalg.inv(A)
    bvs = np.zeros(R.shape[:3])
    for i, sm in enumerate(sym):
        if sm not in BV:
            continue
        R0, bb = BV[sm]
        dfA = (R - frac[i] @ A) @ invA
        dfA -= np.round(dfA)
        d = np.linalg.norm(dfA @ A, axis=-1)
        bvs += np.exp((R0 - d) / bb)
    return (bvs - 1.0) ** 2, ns


def perc_axis(mask, ax):
    N = mask.shape[ax]
    big = np.concatenate([mask, mask], axis=ax)
    lbl, nlab = ndimage.label(big)
    for k in range(1, nlab + 1):
        idx = np.where(lbl == k)[ax]
        if idx.size and (idx.max() - idx.min()) >= N:
            return True
    return False


def perc_onsets(bvse, levels=np.arange(0.05, 3.01, 0.05)):
    m0 = bvse - bvse.min()
    out = {}
    for ax, name in enumerate("abc"):
        out[name] = None
        for E in levels:
            if perc_axis(m0 <= E, ax):
                out[name] = round(float(E), 2); break
    return out


def iso_fractions(bvse):
    m0 = bvse - bvse.min()
    return {str(i): round(100.0 * float((m0 <= i).mean()), 2) for i in ISOS}


# ---------- faithful cubic approximant ----------
def faithful_cubic(A, frac, sym, N, must_have=(), tag="", forbid_B=False):
    p3 = A[2] / N
    C = np.array([A[1] + p3 - A[0], A[0] + p3 - A[1], A[0] + A[1] - p3])
    lens = np.linalg.norm(C, axis=1)
    ang = [math.degrees(math.acos(np.dot(C[i], C[j])/(lens[i]*lens[j])))
           for i, j in ((1, 2), (0, 2), (0, 1))]
    print(f"  [{tag}] C-cell a,b,c = {lens.round(3)}  angles = {np.round(ang,2)}")
    invC = np.linalg.inv(C)
    imgs = []
    for n1 in range(-2, 3):
        for n2 in range(-2, 3):
            for n3 in range(-2, 3):
                imgs.append((n1, n2, n3))
    # composition target: (VolC/VolA) * counts
    ratio = abs(np.linalg.det(C) / np.linalg.det(A))
    from collections import Counter
    cnt_all = Counter(sym)
    target = {e: ratio * c for e, c in cnt_all.items()}
    best = None
    for o1 in np.arange(0, 1, 0.1):
        for o2 in np.arange(0, 1, 0.1):
            for o3 in np.arange(0, 1, 0.1):
                org = (np.array([o1, o2, o3]) + 1e-4) @ A     # cartesian origin
                keep = []
                for (n1, n2, n3) in imgs:
                    r = (frac + np.array([n1, n2, n3])) @ A - org
                    fC = r @ invC
                    ok = np.all((fC >= 0) & (fC < 1), axis=1)
                    for i in np.where(ok)[0]:
                        keep.append((sym[i], fC[i]))
                cc = Counter(s for s, _ in keep)
                if any(cc.get(e, 0) < n for e, n in must_have):
                    continue
                if forbid_B and cc.get("B", 0) > 0:
                    continue
                score = sum(abs(cc.get(e, 0) - target[e]) for e in target)
                score += 2.0 * abs(cc.get("P", 0) - round(target["P"]))
                if best is None or score < best[0]:
                    best = (score, (o1, o2, o3), keep, dict(cc))
    score, org, keep, comp = best
    print(f"  [{tag}] origin {org} composition {comp} (target ~{ {e: round(v,1) for e,v in target.items()} }) score {score:.2f}")
    symC = [s for s, _ in keep]
    fracC = np.array([f for _, f in keep])
    org_cart = (np.array(org) + 1e-4) @ A
    return C, fracC, symC, comp, lens, ang, org_cart


# ---------- exports ----------
def write_cube(fn, title, C, frac, sym, vol):
    ns = vol.shape
    with open(fn, "w") as f:
        f.write(f"{title}\nBVSE aboveMin (valence^2)\n")
        f.write(f"{len(sym):5d} 0.000000 0.000000 0.000000\n")
        for k in range(3):
            v = C[k] / ns[k] / BOHR
            f.write(f"{ns[k]:5d} {v[0]:.6f} {v[1]:.6f} {v[2]:.6f}\n")
        cart = frac @ C / BOHR
        for s, r in zip(sym, cart):
            z = ZNUM[s]
            f.write(f"{z:5d} {float(z):.6f} {r[0]:.6f} {r[1]:.6f} {r[2]:.6f}\n")
        flat = vol.reshape(-1)   # ix outer, iz fastest == C order
        for i in range(0, flat.size, 6):
            f.write(" ".join(f"{x:.5E}" for x in flat[i:i+6]) + "\n")


SITE = {"Li": ("1.5700", "134 224 116 134 224 116"), "P": ("0.5000", "128 110 180 204 191 224"),
        "B": ("0.4500", "255 120 160 244 180 205"), "S": ("1.0000", "255 237  35 255 250   0"),
        "O": ("0.5800", "255  50  30 254   3   0"), "Cl": ("0.9000", " 49 191  49  49 252   2")}


def write_vesta(fn, title, cubefile, lens, ang, frac, sym, iso=0.5):
    cnt = {}
    labels = []
    for s in sym:
        cnt[s] = cnt.get(s, 0) + 1
        labels.append(f"{s}{cnt[s]}")
    els = [e for e in ("Li", "P", "B", "S", "O", "Cl") if e in cnt]
    L = ["#VESTA_FORMAT_VERSION 3.5.4\n\n\nCRYSTAL\n\nTITLE\n" + title + "\n",
         "\nIMPORT_DENSITY 1\n+1.000000 ./" + cubefile + "\n",
         """
GROUP
1 1 P 1
SYMOP
 0.000000  0.000000  0.000000  1  0  0   0  1  0   0  0  1   1
 -1.0 -1.0 -1.0  0 0 0  0 0 0  0 0 0
TRANM 0
 0.000000  0.000000  0.000000  1  0  0   0  1  0   0  0  1
LTRANSL
 -1
 0.000000  0.000000  0.000000  0.000000  0.000000  0.000000
LORIENT
 -1   0   0   0   0
 1.000000  0.000000  0.000000  1.000000  0.000000  0.000000
 0.000000  0.000000  1.000000  0.000000  0.000000  1.000000
LMATRIX
 1.000000  0.000000  0.000000  0.000000
 0.000000  1.000000  0.000000  0.000000
 0.000000  0.000000  1.000000  0.000000
 0.000000  0.000000  0.000000  1.000000
 0.000000  0.000000  0.000000
CELLP
"""]
    L.append(" %9.6f  %9.6f  %9.6f  %9.6f  %9.6f  %9.6f\n" % (lens[0], lens[1], lens[2], ang[0], ang[1], ang[2]))
    L.append("  0.000000   0.000000   0.000000   0.000000   0.000000   0.000000\nSTRUC\n")
    for i, (s, f, lb) in enumerate(zip(sym, frac, labels)):
        L.append("%3d %-2s %10s  1.0000   %8.6f   %8.6f   %8.6f    1a       1\n" % (i+1, s, lb, f[0], f[1], f[2]))
        L.append("                            0.000000   0.000000   0.000000  0.00\n")
    L.append("  0 0 0 0 0 0 0\nTHERI 1\n")
    for i, lb in enumerate(labels):
        L.append("%3d %10s -0.000000\n" % (i+1, lb))
    L.append("  0 0 0\nSHAPE\n  0       0       0       0   0.000000  0   192   192   192   192\n")
    L.append("BOUND\n       0        1         0        1         0        1\n  0   0   0   0  0\nSBOND\n")
    nb = 1
    for pair, dmax in (("P S", "2.57646"), ("P O", "2.08646"), ("B S", "2.27646"), ("B O", "1.70000")):
        e1, e2 = pair.split()
        if e1 in cnt and e2 in cnt:
            L.append("  %d     %s     %s    0.00000    %s  0  1  1  0  1  0.000  0.000 127 127 127\n" % (nb, e1, e2, dmax))
            nb += 1
    L.append("  0 0 0 0\nSITET\n")
    for i, (s, lb) in enumerate(zip(sym, labels)):
        r, col = SITE[s]
        L.append("%3d %10s  %s %s  50  0\n" % (i+1, lb, r, col))
    L.append("  0 0 0 0 0 0\nVECTR\n 0 0 0 0 0\nVECTT\n 0 0 0 0 0\nSPLAN\n  0   0   0   0\nLBLAT\n -1\nLBLSP\n -1\nDLATM\n -1\nDLBND\n -1\nDLPLY\n -1\nPLN2D\n  0   0   0   0\nATOMT\n")
    for k, e in enumerate(els):
        r, col = SITE[e]
        L.append("%3d %10s  %s %s  50\n" % (k+1, e, r, col))
    L.append("  0 0 0 0 0 0\nSCENE\n 0.996905  0.035801 -0.069984  0.000000\n 0.056498  0.292702  0.954533  0.000000\n 0.054658 -0.955533  0.289773  0.000000\n 0.000000  0.000000  0.000000  1.000000\n  0.000   0.000\n  0.000\n  1.192\nHBOND 0 2\n\n")
    L.append("STYLE\nDISPF 37753794\nMODEL   2  1  0\nSURFS   0  1  1\nSECTS  32  1\nFORMS   0  1\nATOMS   0  0  1\nBONDS   1\nPOLYS   1\nVECTS 1.000000\nFORMP\n  1  1.0   0   0   0\nATOMP\n 24  24   0  50  2.0   0\nBONDP\n  1  16  0.000  0.000 127 127 127\nPOLYP\n  50 1  0.030 150 150 150\n")
    L.append("ISURF\n  1   0        %.1f 255 255   0 127 255\n  0   0   0   0\n" % iso)
    L.append("TEX3P\n  1         -INF         -INF\nSECTP\n  1  4.00000E+00  4.00000E+00  0.00000E+00  0.00000E+00  0.00000E+00  0.00000E+00\nCONTR\n 0.1 -1 1 1 10 -1 2 5\n 2 1 2 1\n   0   0   0\n   0   0   0\n   0   0   0\n   0   0   0\nHKLPP\n 192 1  1.000 255   0 255\nUCOLP\n   0   1  1.000   0   0   0\nCOMPS 0\nLABEL 1    12  1.000 0\nPROJT 0  0.962\nBKGRC\n 255 255 255\nDPTHQ 1 -0.5000  3.5000\n")
    for ln in ("LIGHT0 1", "LIGHT1", "LIGHT2", "LIGHT3"):
        L.append(ln + "\n 1.000000  0.000000  0.000000  0.000000\n 0.000000  1.000000  0.000000  0.000000\n 0.000000  0.000000  1.000000  0.000000\n 0.000000  0.000000  0.000000  1.000000\n 0.000000  0.000000 20.000000  0.000000\n 0.000000  0.000000 -1.000000\n")
        if ln == "LIGHT0 1":
            L.append("  26  26  26 255\n 179 179 179 255\n 255 255 255 255\n")
        else:
            L.append("   0   0   0   0\n   0   0   0   0\n   0   0   0   0\n")
    L.append("SECCL 0\n\nTEXCL 0\n\nATOMM\n 204 204 204 255\n  25.600\nBONDM\n 255 255 255 255\n 128.000\nPOLYM\n 255 255 255 255\n 128.000\nSURFM\n   0   0   0 255\n 128.000\nFORMM\n 255 255 255 255\n 128.000\nHKLPM\n 255 255 255 255\n 128.000\n")
    open(fn, "w").write("".join(L))


def write_vasp(fn, title, C, frac, sym):
    order = [e for e in ("Li", "P", "B", "S", "O", "Cl") if e in sym]
    with open(fn, "w") as f:
        f.write(title + "\n1.0\n")
        for v in C:
            f.write("  %18.10f %18.10f %18.10f\n" % tuple(v))
        f.write(" ".join(order) + "\n")
        f.write(" ".join(str(sum(1 for s in sym if s == e)) for e in order) + "\n")
        f.write("Direct\n")
        for e in order:
            for s, fr in zip(sym, frac):
                if s == e:
                    f.write("  %16.10f %16.10f %16.10f\n" % tuple(fr))


# ---------- run all ----------
systems = {}
systems["modelc"] = dict(load=lambda: load_cube_header(f"{REPO}/db/properties/bvse_modelc/modelc_bvse.cube"),
                         N=5, must=(), title="modelC LPSCl1.6 undoped")
systems["b2o3"] = dict(load=lambda: load_vasp(f"{REPO}/db/structures/b2o3_relaxV0.vasp"),
                       N=10, must=(("B", 1), ("O", 1)), title="B2O3-doped LPSCl1.6 champion")
systems["lpsocl"] = dict(load=lambda: load_vasp(f"{REPO}/db/structures/lpsocl_v0.vasp"),
                         N=5, must=(("O", 1),), title="LPSOCl O-doped LPSCl1.6")
systems["b2o3_bulk"] = dict(load=systems["b2o3"]["load"], N=10, must=(("B", 0),),
                            forbid_B=True, title="B2O3-doped LPSCl1.6 bulk-region box")

results = {}
for name, cfg in systems.items():
    print(f"== {name} ==")
    A, frac, sym = cfg["load"]()
    L = np.linalg.norm(A, axis=1)
    print(f"  cell |a|,|b|,|c| = {L.round(3)}  natoms={len(sym)}  |c|/N={L[2]/cfg['N']:.3f}")
    # original cell
    bv, ns, _ = bvse_map(A, frac, sym, 28)
    fr_o = iso_fractions(bv); po_o = perc_onsets(bv)
    print(f"  orig grid {tuple(ns)}  iso% {fr_o}  perc {po_o}")
    # cubic approximant: atoms = folded cut, map = TRUE crystal BVSE resampled
    C, fracC, symC, comp, lens, ang, org_cart = faithful_cubic(A, frac, sym, cfg["N"], cfg["must"], name, cfg.get("forbid_B", False))
    bvC, nsC = bvse_map_box(C, org_cart, A, frac, sym, 40)
    gmin = float(bv.min())          # reference = ORIGINAL map global min
    m0 = bvC - gmin
    fr_c = {str(i): round(100.0 * float((m0 <= i).mean()), 2) for i in ISOS}
    po_c = {"note": "box crop of the true map - no box-PBC percolation defined"}
    print(f"  cubic grid {tuple(nsC)}  box min-above-global {float(bvC.min())-gmin:.3f}  iso% {fr_c}")
    # exports
    write_cube(os.path.join(OUT, f"{name}_orig_bvse_aboveMin.cube"),
               f"{cfg['title']} ORIGINAL cell BVSE", A, frac, sym, bv - bv.min())
    write_cube(os.path.join(OUT, f"{name}_cubicapprox_bvse_aboveMin.cube"),
               f"{cfg['title']} faithful-cubic crop of true-crystal BVSE", C, fracC, symC, bvC - gmin)
    write_vasp(os.path.join(OUT, f"{name}_cubic_approx.vasp"),
               f"{cfg['title']} faithful-cubic approximant (real relaxed atoms folded)", C, fracC, symC)
    write_vesta(os.path.join(OUT, f"{name}_cubicapprox_bvse.vesta"),
                f"BVSE {cfg['title']} faithful-cubic", f"{name}_cubicapprox_bvse_aboveMin.cube",
                lens, ang, fracC, symC)
    results[name] = dict(natoms_orig=len(sym), grid_orig=[int(x) for x in ns],
                         iso_frac_orig=fr_o, perc_orig=po_o,
                         cubic_lengths_A=[round(float(x), 4) for x in lens],
                         cubic_angles_deg=[round(float(x), 3) for x in ang],
                         cubic_composition=comp, natoms_cubic=len(symC),
                         grid_cubic=[int(x) for x in nsC],
                         iso_frac_cubic=fr_c, perc_cubic=po_c)

json.dump(results, open(os.path.join(OUT, "bvse_orig_vs_cubic.json"), "w"), indent=1)
with open(os.path.join(OUT, "bvse_orig_vs_cubic.csv"), "w") as f:
    f.write("# BVSE Li-channel volume %% (above-min <= iso). orig = as-relaxed cell; cubic = faithful conventional-cubic approximant (real atoms folded)\n")
    f.write("iso_val2," + ",".join(f"{s}_orig,{s}_cubic" for s in results) + "\n")
    for iso in ISOS:
        f.write(f"{iso}," + ",".join(f"{results[s]['iso_frac_orig'][str(iso)]},{results[s]['iso_frac_cubic'][str(iso)]}" for s in results) + "\n")
print("\nALL DONE ->", OUT)
