#!/usr/bin/env python3
"""CDD (charge density difference) blue/yellow figures from a Gaussian-cube of
Delta-rho = rho_SCF - rho_atomic.

Produces:
  <out>_3d.png   3D isosurface: YELLOW = electron accumulation (+drho),
                 BLUE = depletion (-drho), atoms overlaid.
  <out>_slice.png 2D slice at the plane of maximum |drho| (diverging map).

Usage:
  python3 plot_cdd.py --cube comp1_cdd.cube --out comp1_cdd \
      --iso 0.006 --label "LPSCl (comp1)"
"""
import argparse
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import TwoSlopeNorm, LinearSegmentedColormap
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

BOHR = 0.5291772108
ELEM_COLOR = {"Li": "#2b2b2b", "P": "#FF8C00", "S": "#E6C200", "Cl": "#3E8E41", "N": "#3F7BB6"}
ELEM_R = {"Li": 0.55, "P": 0.85, "S": 0.85, "Cl": 0.90, "N": 0.70}
PT = {3: "Li", 6: "C", 7: "N", 8: "O", 15: "P", 16: "S", 17: "Cl"}


def read_cube(path):
    L = Path(path).read_text().splitlines()
    nat = int(L[2].split()[0])
    origin = np.array([float(x) for x in L[2].split()[1:4]]) * BOHR
    gn, vox = [], []
    for i in range(3):
        p = L[3 + i].split()
        gn.append(int(p[0])); vox.append([float(x) for x in p[1:4]])
    vox = np.array(vox) * BOHR
    atoms = []
    for i in range(nat):
        p = L[6 + i].split()
        atoms.append((PT.get(int(p[0]), "X"), np.array([float(x) for x in p[2:5]]) * BOHR))
    raw = " ".join(L[6 + nat:]).split()
    data = np.array(raw, float).reshape(gn)
    return data, origin, vox, atoms


def sphere(c, r, n=12):
    u = np.linspace(0, 2 * np.pi, n); v = np.linspace(0, np.pi, n)
    return (c[0] + r * np.outer(np.cos(u), np.sin(v)),
            c[1] + r * np.outer(np.sin(u), np.sin(v)),
            c[2] + r * np.outer(np.ones_like(u), np.cos(v)))


def fig_3d(data, origin, vox, atoms, iso, out, label):
    from skimage.measure import marching_cubes
    fig = plt.figure(figsize=(9, 8)); ax = fig.add_subplot(111, projection="3d")
    for level, col, name in [(iso, "#F4D03F", "accumulation +"), (-iso, "#2E86DE", "depletion -")]:
        if not (data.min() < level < data.max()):
            continue
        verts, faces, *_ = marching_cubes(data, level=level)
        vx = origin + verts @ vox
        ax.add_collection3d(Poly3DCollection(vx[faces], alpha=0.45, facecolor=col,
                                             edgecolor="none", linewidth=0))
    for sym, xyz in atoms:
        ax.scatter(*xyz, c=ELEM_COLOR.get(sym, "#888"), s=55, edgecolors="k",
                   linewidths=0.4, depthshade=False)
    cell = vox * np.array(data.shape)[:, None]
    cs = [origin + i * cell[0] + j * cell[1] + k * cell[2]
          for i in (0, 1) for j in (0, 1) for k in (0, 1)]
    cs = np.array(cs)
    for e in [(0,1),(0,2),(0,4),(1,3),(1,5),(2,3),(2,6),(3,7),(4,5),(4,6),(5,7),(6,7)]:
        ax.plot(*cs[list(e)].T, color="#bbb", lw=0.5, alpha=0.5)
    ax.view_init(22, -60)
    mn, mx = cs.min(0), cs.max(0)
    ax.set_xlim(mn[0], mx[0]); ax.set_ylim(mn[1], mx[1]); ax.set_zlim(mn[2], mx[2])
    ax.set_box_aspect(mx - mn)
    ax.set_xlabel("x (Å)"); ax.set_ylabel("y (Å)"); ax.set_zlabel("z (Å)")
    from matplotlib.patches import Patch
    ax.legend(handles=[Patch(facecolor="#F4D03F", label="+Δρ  accumulation (e gain)"),
                       Patch(facecolor="#2E86DE", label="−Δρ  depletion (e loss)")],
              loc="upper left", fontsize=10, framealpha=0.9)
    ax.set_title(f"Charge density difference  (ρ$_{{SCF}}$ − ρ$_{{atomic}}$)  |iso| = {iso} e/bohr³\n{label}",
                 fontsize=12)
    plt.tight_layout(); plt.savefig(out, dpi=200, bbox_inches="tight"); plt.close()
    print("->", out)


def fig_slice(data, origin, vox, atoms, out, label, axis=2):
    # plane (perpendicular to `axis`) with max sum |drho|
    act = np.abs(data).sum(axis=tuple(i for i in range(3) if i != axis))
    k = int(np.argmax(act))
    sl = np.take(data, k, axis=axis)
    # in-plane axes
    ax_ids = [i for i in range(3) if i != axis]
    L0 = vox[ax_ids[0], ax_ids[0]] * data.shape[ax_ids[0]]
    L1 = vox[ax_ids[1], ax_ids[1]] * data.shape[ax_ids[1]]
    cmap = LinearSegmentedColormap.from_list("bwy",
            ["#1B4F9C", "#4A90D9", "#FFFFFF", "#F4D03F", "#C99A00"])
    vmax = np.percentile(np.abs(sl), 99.7)
    norm = TwoSlopeNorm(vmin=-vmax, vcenter=0, vmax=vmax)
    fig, ax = plt.subplots(figsize=(7.5, 7))
    im = ax.imshow(sl.T, origin="lower", extent=[0, L0, 0, L1], cmap=cmap, norm=norm,
                   interpolation="bilinear")
    # overlay atoms within +/-1.2 A of the slice plane
    zc = origin[axis] + (k + 0.5) * vox[axis, axis]
    for sym, xyz in atoms:
        if abs(xyz[axis] - zc) < 1.3:
            ax.scatter(xyz[ax_ids[0]] - origin[ax_ids[0]], xyz[ax_ids[1]] - origin[ax_ids[1]],
                       s=130, c=ELEM_COLOR.get(sym, "#888"), edgecolors="k", linewidths=0.8)
            ax.annotate(sym, (xyz[ax_ids[0]] - origin[ax_ids[0]], xyz[ax_ids[1]] - origin[ax_ids[1]]),
                        fontsize=8, ha="center", va="center", color="w", weight="bold")
    cb = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cb.set_label("Δρ (e/bohr³)   blue = depletion · yellow = accumulation")
    ax.set_xlabel("Å"); ax.set_ylabel("Å")
    ax.set_title(f"CDD slice (max-activity plane, axis {axis})\n{label}", fontsize=12)
    plt.tight_layout(); plt.savefig(out, dpi=200, bbox_inches="tight"); plt.close()
    print("->", out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cube", required=True); ap.add_argument("--out", required=True)
    ap.add_argument("--iso", type=float, default=0.006)
    ap.add_argument("--label", default="")
    a = ap.parse_args()
    data, origin, vox, atoms = read_cube(a.cube)
    print(f"grid {data.shape}  drho [{data.min():.4f},{data.max():.4f}]  natoms {len(atoms)}")
    fig_3d(data, origin, vox, atoms, a.iso, a.out + "_3d.png", a.label)
    fig_slice(data, origin, vox, atoms, a.out + "_slice.png", a.label)


if __name__ == "__main__":
    main()
