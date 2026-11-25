#!/usr/bin/env python3
"""Sample ELF at bond midpoints from a QE plot_num=8 cube -> covalency CSV.

Self-contained: reads only the .cube (atoms + ELF grid). For every atom pair
within an element-pair distance cutoff it computes the PBC minimum-image
midpoint and the ELF there (trilinear, periodic), plus ELF at 1/4 and 3/4
along the bond. Groups by bond type and writes mean values.

ELF reading: midpoint ELF ~0.7-0.9 = covalent bond pair; ~0.3-0.5 = ionic/
free-electron; <0.3 = depleted. So P-S (covalent) >> Li-S, Li-Cl (ionic).

Usage:
    python3 sample_elf_bonds.py --cube X.cube --system comp1 --out elf_bonds.csv
    python3 sample_elf_bonds.py --selftest

Minimum image (2026-10-19 fix): rounding the fractional difference alone is NOT the minimum image in a
skewed cell. The Sept Nd@Li cell (60 deg angles, c = 69 A) lost one Nd-S bond that way (3.141 A read as
5.234 A -> 7 of 8 Nd-S). `make_mic` rounds, then searches the neighbouring images; the search width
n_i = ceil(rmax*|b_i|) + 1 (b_i = reciprocal vector without 2 pi) covers every image within rmax.
In an orthogonal cell the result is identical to plain rounding, so the cubic host tables
(modelc / b2o3 / lpsocl) are unchanged.

What this tool cannot do: it reports ELF at fixed fractions of each bond (midpoint, [0.4, 0.6] minimum);
it does not find ELF basins or attractors, and a midpoint value near 0.5 does not by itself say
"no bond" (the midpoint of a long cation-anion bond can sit outside the anion's lone-pair region).
"""
import argparse
import itertools
import numpy as np

BOHR = 0.5291772108
PT = {3: "Li", 5: "B", 6: "C", 7: "N", 8: "O", 9: "F", 11: "Na",
      15: "P", 16: "S", 17: "Cl", 20: "Ca", 35: "Br", 60: "Nd"}
# element-pair cutoffs (Å) for "a bond" -- KEYS MUST BE alphabetically sorted
# B-S ~1.9 (thioborate BS3 motif), B-O ~1.4 (borate BO3) -- the B2O3-dopant bonds.
# Nd-S / Cl-Nd 3.3 (2026-10-19 · Nd Q3 ELF): the Bader site rule fixed before results (R_NdX 3.3 A,
# runlog nd_q3_bader_elf_runlog_2026_10_19.json) -- Sept new-PP Nd@Li cell: 8 Nd-S (2.61-3.14) · 2 Cl-Nd · next S 3.38.
CUT = {("P", "S"): 2.3, ("Li", "S"): 2.9, ("Cl", "Li"): 2.95,
       ("S", "S"): 3.0, ("O", "P"): 1.9, ("Nd", "O"): 2.8, ("Li", "O"): 2.5,
       ("Nd", "S"): 3.3, ("Cl", "Nd"): 3.3,
       ("B", "S"): 2.15, ("B", "O"): 1.7, ("B", "B"): 2.0}


def read_cube(path):
    L = open(path).read().splitlines()
    nat = int(L[2].split()[0])
    origin = np.array([float(x) for x in L[2].split()[1:4]]) * BOHR
    gn, vox = [], []
    for i in range(3):
        p = L[3 + i].split()
        gn.append(int(p[0]))
        vox.append([float(x) for x in p[1:4]])
    vox = np.array(vox) * BOHR
    gn = np.array(gn)
    cell = vox * gn[:, None]                      # rows = lattice vectors (Å)
    atoms = []
    for i in range(nat):
        p = L[6 + i].split()
        atoms.append((PT.get(int(p[0]), str(p[0])),
                      np.array([float(x) for x in p[2:5]]) * BOHR))
    raw = " ".join(L[6 + nat:]).split()
    data = np.array(raw, float).reshape(gn[0], gn[1], gn[2])
    return data, origin, cell, gn, atoms


def elf_at(data, gn, cell_inv, origin, r):
    """Trilinear, periodic ELF at Cartesian point r."""
    f = (cell_inv @ (r - origin)) % 1.0          # fractional, wrapped
    g = f * gn
    i0 = np.floor(g).astype(int)
    d = g - i0
    val = 0.0
    for dx in (0, 1):
        for dy in (0, 1):
            for dz in (0, 1):
                w = (d[0] if dx else 1 - d[0]) * (d[1] if dy else 1 - d[1]) * (d[2] if dz else 1 - d[2])
                ix = (i0[0] + dx) % gn[0]
                iy = (i0[1] + dy) % gn[1]
                iz = (i0[2] + dz) % gn[2]
                val += w * data[ix, iy, iz]
    return val


def make_mic(cell, rmax):
    """Minimum-image displacement for any cell (rows = lattice vectors, A).
    Round the fractional difference, then take the shortest of the neighbouring images
    s_i in [-n_i, n_i], n_i = ceil(rmax*|b_i|) + 1 -- every image within rmax is searched."""
    cell_inv = np.linalg.inv(cell.T)
    recip = np.linalg.inv(cell).T                # rows b_i with a_i . b_j = delta_ij
    n = [int(np.ceil(rmax * np.linalg.norm(recip[i]))) + 1 for i in range(3)]
    shifts = np.array(list(itertools.product(*[range(-k, k + 1) for k in n])), float)

    def mic(rij):
        f = cell_inv @ rij
        f -= np.round(f)
        cand = (f + shifts) @ cell
        return cand[int(np.argmin(np.einsum("ij,ij->i", cand, cand)))]
    return mic


def selftest():
    fails = []

    def ck(name, cond):
        print(f"  {'ok ' if cond else 'BAD'} {name}")
        if not cond:
            fails.append(name)
    # the Sept Nd@Li cell (scf_input_copy.in, db/raw/nd_q3_bader_2026_10_19) and its Nd1 / S44 pair
    cell = np.array([[6.9981521450, -0.0038493990, -0.0076859570],
                     [3.4203457800, 6.0142217730, 0.0014754540],
                     [34.6984274870, 19.6853743570, 56.8750722600]])
    nd = np.array([6.0652079823, 6.2641664098, 5.7451996488])
    s44 = np.array([8.3091056391, 5.4722628589, 3.6942688291])
    rmax = max(CUT.values())
    d_new = np.linalg.norm(make_mic(cell, rmax)(s44 - nd))
    f = np.linalg.inv(cell.T) @ (s44 - nd)
    d_round = np.linalg.norm(cell.T @ (f - np.round(f)))
    ck(f"skewed Nd cell: Nd1-S44 = 3.141 A (got {d_new:.3f})", abs(d_new - 3.141) < 5e-4)
    ck(f"negative: plain rounding reads it as 5.234 A (got {d_round:.3f}) -- the bug this fixes",
       abs(d_round - 5.234) < 5e-4)
    rng = np.random.default_rng(3)
    v = rng.normal(size=(200, 3))
    v = v / np.linalg.norm(v, axis=1)[:, None] * rng.uniform(0.5, rmax, (200, 1))   # a true image within rmax
    rs = v + rng.integers(-3, 4, (200, 3)) @ cell                                    # hidden behind lattice shifts
    ci = np.linalg.inv(cell.T)
    brute = [min(np.linalg.norm(cell.T @ (ci @ r - np.round(ci @ r) + np.array(t)))
                 for t in itertools.product(range(-5, 6), repeat=3)) for r in rs]
    mic = make_mic(cell, rmax)
    got = [np.linalg.norm(mic(r)) for r in rs]
    ck("skewed cell: 200 pairs with an image inside rmax -- search == +-5 brute force, and <= the planted length",
       all(abs(g - b) < 1e-9 for g, b in zip(got, brute)) and all(g <= np.linalg.norm(x) + 1e-9 for g, x in zip(got, v)))
    rnd = [np.linalg.norm(cell.T @ (ci @ r - np.round(ci @ r))) for r in rs]
    ck(f"negative: plain rounding misses some of them ({sum(1 for a, b in zip(rnd, brute) if a - b > 1e-6)} of 200)",
       any(a - b > 1e-6 for a, b in zip(rnd, brute)))
    cub = np.eye(3) * 10.0
    mc = make_mic(cub, rmax)
    rr = rng.uniform(-20, 20, (40, 3))
    same = all(np.allclose(mc(r), cub.T @ ((np.linalg.inv(cub.T) @ r) - np.round(np.linalg.inv(cub.T) @ r))) for r in rr
               if np.linalg.norm(cub.T @ ((np.linalg.inv(cub.T) @ r) - np.round(np.linalg.inv(cub.T) @ r))) < 4.9)
    ck("orthogonal cell: identical to plain rounding (host tables unchanged)", same)
    print(f"selftest {'PASS' if not fails else 'FAIL'} ({len(fails)} fail)")
    return 0 if not fails else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cube")
    ap.add_argument("--system")
    ap.add_argument("--out")
    ap.add_argument("--append", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()
    if args.selftest:
        raise SystemExit(selftest())
    if not (args.cube and args.system and args.out):
        ap.error("--cube --system --out are required (or --selftest)")

    data, origin, cell, gn, atoms = read_cube(args.cube)
    cell_inv = np.linalg.inv(cell.T)             # so cell_inv @ r = fractional
    syms = [a[0] for a in atoms]
    pos = np.array([a[1] for a in atoms])
    n = len(atoms)
    mic = make_mic(cell, max(CUT.values()))      # minimum image -- correct in skewed cells too

    acc = {}
    for i in range(n):
        for j in range(i + 1, n):
            key = tuple(sorted([syms[i], syms[j]]))
            if key not in CUT:
                continue
            rij = mic(pos[j] - pos[i])
            dist = np.linalg.norm(rij)
            if dist > CUT[key]:
                continue
            # ELF at the bond MIDPOINT is the covalency descriptor here:
            #   P-S (covalent) ~0.94 > Li-S ~0.93 > Li-Cl ~0.85 (more ionic).
            # (The wider-line minimum just hits the atomic core-valence shell
            #  node ~0.05 and is NOT a bond property, so we report the central
            #  [0.4,0.6] minimum as a robustness check alongside the midpoint.)
            e_mid = elf_at(data, gn, cell_inv, origin, pos[i] + rij * 0.5)
            ts = np.linspace(0.40, 0.60, 9)
            e_cmin = float(np.min([elf_at(data, gn, cell_inv, origin,
                                          pos[i] + rij * t) for t in ts]))
            lab = "-".join(key)
            acc.setdefault(lab, []).append((dist, e_mid, e_cmin))

    rows = []
    for lab, vals in sorted(acc.items()):
        v = np.array(vals)
        rows.append((args.system, lab, len(v), v[:, 0].mean(),
                     v[:, 1].mean(), v[:, 1].std(), v[:, 2].mean()))

    hdr = "system,bond,n_bonds,mean_dist_A,ELF_midpoint,ELF_mid_std,ELF_central_min\n"
    mode = "a" if args.append else "w"
    with open(args.out, mode) as f:
        if not args.append:
            f.write(hdr)
        for r in rows:
            f.write(f"{r[0]},{r[1]},{r[2]},{r[3]:.3f},{r[4]:.3f},{r[5]:.3f},{r[6]:.3f}\n")
    print(f"[{args.system}] ELF midpoint (covalency: P-S > Li-S > Li-Cl):")
    for r in rows:
        print(f"  {r[1]:7s} n={r[2]:4d}  d={r[3]:.2f}A  ELF_mid={r[4]:.3f}±{r[5]:.3f}")
    print(f"-> {args.out}")


if __name__ == "__main__":
    main()
