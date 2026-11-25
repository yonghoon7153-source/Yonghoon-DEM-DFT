#!/usr/bin/env python3
"""Montage of ELF slices through several Cl atoms — shows DISORDER directly.

Ordered LPSCl: every Cl has an identical Li cage (panels look copy-pasted).
Cl-rich LPSCl1.6: every Cl is different (varied Li distances, some with a
MISSING Li = vacancy, lower coordination) -> panels look different.

Each panel = ELF on the plane through one Cl + its 2 nearest Li, with a
coordination badge (number of Li within 3.0 A) and the nearest-Li distances.

Usage:
  python3 elf_licl_montage.py --comp1 comp1_ELF.cube --modelc modelc_ELF.cube \
      --out elf_licl_montage.png
"""
import argparse
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

BOHR = 0.5291772108
ELEM_COLOR = {"Li": "#7b2fbe", "P": "#FF9933", "S": "#FFDC52", "Cl": "#3E8E41"}
PT = {3: "Li", 7: "N", 8: "O", 15: "P", 16: "S", 17: "Cl", 60: "Nd"}


def read_cube(path):
    L = open(path).read().splitlines()
    nat = int(L[2].split()[0])
    origin = np.array([float(x) for x in L[2].split()[1:4]]) * BOHR
    gn, vox = [], []
    for i in range(3):
        p = L[3 + i].split()
        gn.append(int(p[0])); vox.append([float(x) for x in p[1:4]])
    gn = np.array(gn); cell = np.array(vox) * BOHR * gn[:, None]
    atoms = []
    for i in range(nat):
        p = L[6 + i].split()
        atoms.append((PT.get(int(p[0]), str(p[0])),
                      np.array([float(x) for x in p[2:5]]) * BOHR))
    data = np.array(" ".join(L[6 + nat:]).split(), float).reshape(*gn)
    return data, origin, cell, gn, atoms


def elf_cmap():
    return mcolors.LinearSegmentedColormap.from_list("ELF", [
        "#08306b", "#08519c", "#2171b5", "#6baed6", "#41ab5d",
        "#fee08b", "#fdae61", "#d73027", "#a50026"])


def panel(ax, cube, iCl, H=3.6, N=170):
    data, origin, cell, gn, atoms = cube
    cinvT = np.linalg.inv(cell.T)
    syms = [a[0] for a in atoms]; pos = np.array([a[1] for a in atoms])

    def mic(d):
        f = cinvT @ d; f -= np.round(f); return cell.T @ f

    def elf_at(r):
        f = (cinvT @ (r - origin)) % 1.0
        g = f * gn; i0 = np.floor(g).astype(int); d = g - i0
        v = 0.0
        for dx in (0, 1):
            for dy in (0, 1):
                for dz in (0, 1):
                    w = ((d[0] if dx else 1-d[0])*(d[1] if dy else 1-d[1])*(d[2] if dz else 1-d[2]))
                    v += w * data[(i0[0]+dx) % gn[0], (i0[1]+dy) % gn[1], (i0[2]+dz) % gn[2]]
        return v

    Ld = sorted((np.linalg.norm(mic(pos[k] - pos[iCl])), k)
                for k in range(len(atoms)) if syms[k] == "Li")
    coord = sum(1 for d, _ in Ld if d < 3.0)
    p0 = pos[iCl]
    l1 = p0 + mic(pos[Ld[0][1]] - p0); l2 = p0 + mic(pos[Ld[1][1]] - p0)
    e1 = (l1 - p0); e1 /= np.linalg.norm(e1)
    nrm = np.cross(e1, l2 - p0); nrm /= np.linalg.norm(nrm)
    e2 = np.cross(nrm, e1); e2 /= np.linalg.norm(e2)
    us = np.linspace(-H, H, N)
    img = np.array([[elf_at(p0 + u*e1 + v*e2) for u in us] for v in us])
    ax.imshow(img, origin="lower", extent=[-H, H, -H, H], cmap=elf_cmap(),
              vmin=0, vmax=1, aspect="equal", interpolation="bilinear")
    ax.contour(us, us, img, levels=[0.5], colors="white", linewidths=0.7, linestyles="--")
    for k in range(len(atoms)):
        d = mic(pos[k] - p0)
        u, v, w = np.dot(d, e1), np.dot(d, e2), np.dot(d, nrm)
        if abs(w) > 1.4 or abs(u) > H or abs(v) > H:
            continue
        ax.plot(u, v, "o", mfc=ELEM_COLOR.get(syms[k], "#888"), mec="white", mew=0.8,
                ms=9 if syms[k] == "Cl" else 7, zorder=5)
    ax.set_xticks([]); ax.set_yticks([])
    badge = "red" if coord < 6 else "white"
    ax.text(0.04, 0.96, f"Cl#{iCl+1}\ncoord {coord}", transform=ax.transAxes,
            va="top", ha="left", fontsize=9, color="black", fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.2", fc=badge, alpha=0.85, ec="k"))
    near = ", ".join(f"{d:.2f}" for d, _ in Ld[:coord])
    ax.set_xlabel(f"Li @ {near} Å", fontsize=7)
    return coord


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--comp1", required=True); ap.add_argument("--modelc", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--comp1_cl", type=int, nargs="+", default=[45, 46, 47])
    ap.add_argument("--modelc_cl", type=int, nargs="+", default=[53, 59, 62])
    args = ap.parse_args()

    c1 = read_cube(args.comp1); mc = read_cube(args.modelc)
    nc = max(len(args.comp1_cl), len(args.modelc_cl))
    fig, axs = plt.subplots(2, nc, figsize=(3.3 * nc, 7.0))
    im = None
    for j, cl in enumerate(args.comp1_cl):
        panel(axs[0, j], c1, cl - 1)
    for j, cl in enumerate(args.modelc_cl):
        panel(axs[1, j], mc, cl - 1)
    axs[0, 0].set_ylabel("comp1  LPSCl\n(ordered)", fontsize=12, fontweight="bold")
    axs[1, 0].set_ylabel("modelc  LPSCl$_{1.6}$\n(Cl-rich + disorder)", fontsize=12, fontweight="bold")
    fig.suptitle("ELF around different Cl atoms — comp1: every Cl IDENTICAL (coord 6)  |  "
                 "modelc: every Cl DIFFERENT, Cl#53 has a MISSING Li (coord 4 = vacancy)",
                 fontsize=11.5, y=0.99)
    # shared colorbar
    sm = plt.cm.ScalarMappable(cmap=elf_cmap(), norm=mcolors.Normalize(0, 1))
    fig.colorbar(sm, ax=axs, fraction=0.025, pad=0.01, label="ELF")
    fig.savefig(args.out, dpi=190, facecolor="white", bbox_inches="tight")
    print(f"-> {args.out}")


if __name__ == "__main__":
    main()
