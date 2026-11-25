#!/usr/bin/env python3
"""Compare Li density .cube files: 2D max-projection heatmaps + connectivity stats.

A VESTA 3D isosurface is the publication figure; this gives a quick programmatic
comparison (top-view Li-density projection + % of cell occupied above thresholds)
so comp1 (LPSCl) vs modelc (LPSCl1.6) Li-network spread can be quantified.

Usage:
  python3 plot_cube_compare.py comp1=comp1.cube modelc=modelc.cube \
      --axis 2 --out plot.png
"""
import argparse, re, sys
import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt


def read_cube(path):
    L = open(path).read().splitlines()
    nat = int(L[2].split()[0])
    n = [int(L[3 + i].split()[0]) for i in range(3)]
    data = []
    for ln in L[6 + nat:]:
        data += [float(x) for x in ln.split()]
    rho = np.array(data).reshape(n)        # (n0,n1,n2)
    return rho, n


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pairs", nargs="+", help="label=path.cube")
    ap.add_argument("--axis", type=int, default=2, help="project (max) along this axis")
    ap.add_argument("--out", default="cube_compare.png")
    args = ap.parse_args()

    cubes = []
    for it in args.pairs:
        lab, path = it.split("=", 1)
        rho, n = read_cube(path)
        cubes.append((lab, rho, n))

    print(f"{'system':<10}{'grid':>14}{'rho_max':>10}{'>0.2max%':>10}{'>0.3max%':>10}{'>0.5max%':>10}")
    print("=" * 64)
    for lab, rho, n in cubes:
        mx = rho.max()
        s = {f: round(float((rho > f * mx).mean()) * 100, 2) for f in (0.2, 0.3, 0.5)}
        print(f"{lab:<10}{str(tuple(n)):>14}{mx:>10.4f}{s[0.2]:>10}{s[0.3]:>10}{s[0.5]:>10}")

    fig, axs = plt.subplots(1, len(cubes), figsize=(5.5 * len(cubes), 5))
    if len(cubes) == 1:
        axs = [axs]
    for ax, (lab, rho, n) in zip(axs, cubes):
        proj = rho.max(axis=args.axis)        # max-projection (Li network footprint)
        im = ax.imshow(proj.T, origin="lower", cmap="viridis", aspect="auto")
        ax.set_title(f"{lab}  (Li density max-proj, axis {args.axis})", fontsize=10)
        ax.set_xticks([]); ax.set_yticks([])
        fig.colorbar(im, ax=ax, fraction=0.046)
    fig.tight_layout(); fig.savefig(args.out, dpi=200)
    print(f"\n-> {args.out}")


if __name__ == "__main__":
    main()
