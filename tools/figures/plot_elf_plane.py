#!/usr/bin/env python3
"""ELF on an ARBITRARY plane through a PS4 tetrahedron (cell-shape independent).

Axial (xy/xz/yz) slices distort non-orthogonal cells (modelC rhombo -> trapezoid).
This samples ELF on a plane defined by 3 atoms (P + 2 S of a PS4), giving a clean
undistorted square view of the P-S covalent bonds, comparable across cells.

Auto-picks a P atom + its 2 nearest S if --atoms not given. Trilinear, periodic
interpolation of the cube onto a regular in-plane grid centered on the P.

Usage:
    python3 plot_elf_plane.py --cube X.cube --out Y.png --label "modelC (LPSCl1.6)"
    python3 plot_elf_plane.py --cube X.cube --out Y.png --atoms 1 5 9   # P S S (1-based)
"""
import argparse
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

BOHR = 0.5291772108
PT = {3: "Li", 6: "C", 7: "N", 8: "O", 9: "F", 11: "Na",
      15: "P", 16: "S", 17: "Cl", 20: "Ca", 35: "Br", 60: "Nd"}
ELEM_COLOR = {"Li": "#1a1a1a", "P": "#FF9933", "S": "#FFDC52", "Cl": "#3E8E41",
              "O": "#E8482B", "Nd": "#46c2c2"}


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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cube", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--label", default="")
    ap.add_argument("--atoms", type=int, nargs=3, default=None,
                    help="1-based P S S indices defining the plane")
    ap.add_argument("--half", type=float, default=4.0, help="half-window (Å)")
    ap.add_argument("--n", type=int, default=240, help="grid points/side")
    ap.add_argument("--thickness", type=float, default=1.3,
                    help="show atoms within this Å of the plane")
    args = ap.parse_args()

    data, origin, cell, gn, atoms = read_cube(args.cube)
    cell_inv = np.linalg.inv(cell.T)
    syms = [a[0] for a in atoms]; pos = np.array([a[1] for a in atoms])

    def mic(d):
        f = cell_inv @ d; f -= np.round(f); return cell.T @ f

    # choose P + 2 S
    if args.atoms:
        iP, iS1, iS2 = [k - 1 for k in args.atoms]
        s1 = pos[iP] + mic(pos[iS1] - pos[iP])
        s2 = pos[iP] + mic(pos[iS2] - pos[iP])
        p0 = pos[iP]
    else:
        Ps = [k for k in range(len(atoms)) if syms[k] == "P"]
        iP = Ps[len(Ps) // 2]                      # a central-ish P
        p0 = pos[iP]
        Sd = sorted(((np.linalg.norm(mic(pos[k] - p0)), k)
                     for k in range(len(atoms)) if syms[k] == "S"))
        s1 = p0 + mic(pos[Sd[0][1]] - p0)
        s2 = p0 + mic(pos[Sd[1][1]] - p0)
    print(f"plane P=atom{iP+1} ; P-S1={np.linalg.norm(s1-p0):.2f} "
          f"P-S2={np.linalg.norm(s2-p0):.2f} Å")

    # in-plane orthonormal basis (e1 along P->S1, e2 perp in P-S1-S2 plane)
    e1 = (s1 - p0); e1 /= np.linalg.norm(e1)
    t = (s2 - p0)
    nrm = np.cross(e1, t); nrm /= np.linalg.norm(nrm)
    e2 = np.cross(nrm, e1); e2 /= np.linalg.norm(e2)

    H, N = args.half, args.n
    us = np.linspace(-H, H, N)
    img = np.zeros((N, N))
    for iy, v in enumerate(us):
        for ix, u in enumerate(us):
            r = p0 + u * e1 + v * e2
            f = (cell_inv @ (r - origin)) % 1.0
            g = f * gn; i0 = np.floor(g).astype(int); d = g - i0
            val = 0.0
            for dx in (0, 1):
                for dy in (0, 1):
                    for dz in (0, 1):
                        w = ((d[0] if dx else 1 - d[0]) * (d[1] if dy else 1 - d[1])
                             * (d[2] if dz else 1 - d[2]))
                        val += w * data[(i0[0]+dx) % gn[0], (i0[1]+dy) % gn[1], (i0[2]+dz) % gn[2]]
            img[iy, ix] = val

    fig, ax = plt.subplots(figsize=(7.5, 7))
    im = ax.imshow(img, origin="lower", extent=[-H, H, -H, H], cmap=elf_cmap(),
                   vmin=0, vmax=1, aspect="equal", interpolation="bilinear")
    cb = plt.colorbar(im, ax=ax, shrink=0.85, pad=0.02); cb.set_label("ELF", fontsize=12)
    ax.contour(us, us, img, levels=[0.5, 0.75], colors=["white", "black"],
               linewidths=[1.0, 1.0], linestyles=["--", "-"])
    # overlay atoms near the plane
    for k in range(len(atoms)):
        r = p0 + mic(pos[k] - p0)
        d = r - p0
        u, v, w = np.dot(d, e1), np.dot(d, e2), np.dot(d, nrm)
        if abs(w) > args.thickness or abs(u) > H or abs(v) > H:
            continue
        c = ELEM_COLOR.get(syms[k], "#888")
        ax.plot(u, v, "o", mfc=c, mec="white", mew=0.9, ms=9, zorder=5)
        ax.text(u + 0.18, v + 0.18, syms[k], fontsize=8, color="white", zorder=6,
                bbox=dict(boxstyle="round,pad=0.12", fc="black", alpha=0.55, ec="none"))
    ax.set_xlabel("in-plane x (Å)"); ax.set_ylabel("in-plane y (Å)")
    ax.set_title(f"ELF on PS$_4$ plane — {args.label}", fontsize=12)
    plt.tight_layout()
    plt.savefig(args.out, dpi=220, facecolor="white", bbox_inches="tight")
    print(f"-> {args.out}")


if __name__ == "__main__":
    main()
