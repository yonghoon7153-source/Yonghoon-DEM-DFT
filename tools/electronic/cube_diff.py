#!/usr/bin/env python3
"""Charge-density-difference (CDD) and generic cube arithmetic — pure numpy.

CDD:  Δρ = ρ(AB) − ρ(A) − ρ(B)   (bonding/charge-transfer; blue=depletion, yellow=accumulation)
or simple difference ρ(1) − ρ(2) for before/after doping.

The three (or two) cubes MUST share the same grid + lattice (run pp.x on the
SAME cell; for fragments, delete atoms but keep the cell/grid identical).

Usage:
  # CDD of A-B bond:  rho_AB - rho_A - rho_B
  python3 cube_diff.py --mode cdd --ab rho_AB.cube --a rho_A.cube --b rho_B.cube --out cdd.cube
  # plain difference (e.g. doped - undoped)
  python3 cube_diff.py --mode sub --a doped.cube --b undoped.cube --out diff.cube
  # also writes a quick 2D max-projection PNG (blue/yellow) for a sanity look

QE side (run on HPC):  pp.x with plot_num=0 (valence charge) for each system →
cube (output_format=6, fileout='rho.cube'). For ELF use plot_num=8.
"""
import argparse, sys
import numpy as np


def read_cube(path):
    L = open(path).read().splitlines()
    nat = int(L[2].split()[0])
    origin = np.array([float(x) for x in L[2].split()[1:4]])
    n, vox = [], []
    for i in range(3):
        t = L[3 + i].split()
        n.append(int(t[0])); vox.append([float(x) for x in t[1:4]])
    header = L[: 6 + nat]
    data = []
    for ln in L[6 + nat:]:
        data += [float(x) for x in ln.split()]
    rho = np.array(data).reshape(n)
    return rho, header, np.array(n), np.array(vox)


def write_cube(path, rho, header):
    with open(path, "w") as f:
        f.write("\n".join(header) + "\n")
        flat = rho.ravel()
        for i in range(0, len(flat), 6):
            f.write("".join(f"{v:13.5e}" for v in flat[i:i + 6]) + "\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["cdd", "sub"], required=True)
    ap.add_argument("--ab"); ap.add_argument("--a", required=True); ap.add_argument("--b", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--png", default=None, help="optional 2D projection PNG")
    ap.add_argument("--axis", type=int, default=2)
    args = ap.parse_args()

    ra, ha, na, _ = read_cube(args.a)
    rb, hb, nb, _ = read_cube(args.b)
    if not np.array_equal(na, nb):
        sys.exit(f"grid mismatch: {tuple(na)} vs {tuple(nb)} — cubes must share the same grid")

    if args.mode == "cdd":
        if not args.ab:
            sys.exit("--ab required for cdd mode")
        rab, hab, nab, _ = read_cube(args.ab)
        if not np.array_equal(nab, na):
            sys.exit("grid mismatch for AB cube")
        diff = rab - ra - rb
        header = hab
    else:
        diff = ra - rb
        header = ha

    write_cube(args.out, diff, header)
    pos = float(diff[diff > 0].sum()); neg = float(diff[diff < 0].sum())
    print(f"-> {args.out}")
    print(f"   Δρ range [{diff.min():.3e}, {diff.max():.3e}] | +sum {pos:.3f} | -sum {neg:.3f} (≈cancel: {pos+neg:.3e})")

    if args.png:
        import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
        proj = diff.sum(axis=args.axis)
        vmax = np.abs(proj).max()
        plt.figure(figsize=(5.5, 5))
        plt.imshow(proj.T, origin="lower", cmap="bwr_r", vmin=-vmax, vmax=vmax, aspect="auto")
        plt.colorbar(label="Δρ (yellow/red=accum, blue=deplet)")
        plt.title("Charge density difference (projection)"); plt.xticks([]); plt.yticks([])
        plt.tight_layout(); plt.savefig(args.png, dpi=180); print(f"-> {args.png}")


if __name__ == "__main__":
    main()
