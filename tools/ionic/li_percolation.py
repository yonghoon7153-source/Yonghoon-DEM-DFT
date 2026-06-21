#!/usr/bin/env python3
"""li_percolation.py — Li-network percolation barrier from a Li-density .cube.

Regenerates docs/figures/elf_licl/Li_percolation_barrier_comp1_modelc.png
(and its CSV) EXACTLY from the time-averaged Li probability density produced by
li_density_cube.py. This is the quantitative version of the "inter-cage" story:
it measures, independent of BVSE, how flat the Li migration landscape is.

Idea
----
Turn the Li probability density rho(r) into a potential of mean force (PMF):

    F(r) = -kT * ln( rho(r) / rho_max )          [eV]   (F=0 at the density peak)

F is the free-energy cost (relative to the most-occupied site) of finding Li at
r. Now raise a "water level" F: the ACCESSIBLE region is every voxel with
F(r) <= F (i.e. rho >= rho_max * exp(-F/kT)). As F rises we flood progressively
lower-density (harder-to-reach) regions. The PERCOLATION THRESHOLD F* is the
smallest F at which the accessible region first SPANS the cell under periodic
boundary conditions — i.e. a continuous Li path connects a cage to its periodic
image. F* is the effective inter-cage migration barrier.

    comp1 (LPSCl)    F* ~ 0.191 eV   (isolated cages, must climb high to connect)
    modelc (LPSCl1.6) F* ~ 0.078 eV  (anti-site disorder flattens inter-cage route)

This reproduces Ea(AIMD) 0.253 -> 0.224 eV INDEPENDENTLY of BVSE, and resolves
the static-channel paradox (BVSE accessible channel is -15% yet sigma x4): the
gain is in the inter-cage bottleneck that BVSE's bond-valence sum misses.

PBC spanning detection
----------------------
A region percolates along axis a iff, tiled 2x2x2 and labelled (6-connectivity,
no PBC), some connected component has bounding-box extent > N_a along a (it
reaches into the periodic copy = wraps around the cell). Cluster sizes for the
y-axis use a separate PBC face-merge union-find on the original (untiled) grid.

Usage (gabia/kserver116-27, the Li-density cubes live there):
  python3 li_percolation.py \
      --cube comp1_Cl1.0_T600_Li.cube:LPSCl \
      --cube modelc_Cl1.6_T600_Li.cube:LPSCl1.6 \
      --T 600 --Fmax 0.30 --dF 0.005 \
      --out ../../docs/figures/elf_licl/percolation_comp1_modelc.csv \
      --plot ../../docs/figures/elf_licl/Li_percolation_barrier_comp1_modelc.png

Needs numpy + scipy (+ matplotlib only if --plot). kT(T) = 8.617333e-5*T eV.
"""
import argparse
import numpy as np

KB = 8.617333262e-5  # eV/K


def read_cube_density(path):
    """Parse a Gaussian .cube (as written by li_density_cube.py) -> rho[na,nb,nc]."""
    with open(path) as f:
        lines = f.read().splitlines()
    natoms = int(lines[2].split()[0])
    n = [int(lines[3 + ax].split()[0]) for ax in range(3)]
    data_start = 6 + abs(natoms)
    vals = []
    for ln in lines[data_start:]:
        s = ln.split()
        if s:
            vals.extend(float(x) for x in s)
    rho = np.array(vals, float).reshape(n[0], n[1], n[2])  # C-order: c fastest
    return rho


def pbc_largest_cluster_frac(mask, struct):
    """Fraction of cell occupied by the largest PBC-connected accessible cluster."""
    from scipy import ndimage
    lab, n = ndimage.label(mask, structure=struct)
    if n == 0:
        return 0.0
    parent = list(range(n + 1))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb

    for ax in range(3):  # merge labels touching across each periodic face
        f0 = np.take(lab, 0, axis=ax)
        f1 = np.take(lab, -1, axis=ax)
        nz = (f0 > 0) & (f1 > 0)
        for a, b in zip(f0[nz].tolist(), f1[nz].tolist()):
            union(a, b)

    cnt = np.bincount(lab.ravel())
    sizes = {}
    for l in range(1, n + 1):
        r = find(l)
        sizes[r] = sizes.get(r, 0) + cnt[l]
    return (max(sizes.values()) / mask.size) * 100.0 if sizes else 0.0


def percolates(mask, struct):
    """Set of axes (0/1/2) the accessible region spans under PBC (2x2x2 tiling)."""
    from scipy import ndimage
    big = np.tile(mask, (2, 2, 2))
    lab, n = ndimage.label(big, structure=struct)
    if n == 0:
        return set()
    N = mask.shape
    axes = set()
    for sl in ndimage.find_objects(lab):
        if sl is None:
            continue
        for ax in range(3):
            if (sl[ax].stop - sl[ax].start) > N[ax]:
                axes.add(ax)
        if len(axes) == 3:
            break
    return axes


def analyse(path, label, F_grid, kT):
    from scipy import ndimage
    struct = ndimage.generate_binary_structure(3, 1)  # 6-connectivity
    rho = read_cube_density(path)
    rho = np.clip(rho, 0.0, None)
    rho_max = rho.max()
    if rho_max <= 0:
        raise SystemExit(f"{path}: empty density")
    # F(r); rho==0 -> +inf (never accessible)
    with np.errstate(divide="ignore"):
        F = -kT * np.log(np.where(rho > 0, rho / rho_max, 1e-300))

    pct = np.empty_like(F_grid)
    F_star = None
    for i, Flevel in enumerate(F_grid):
        mask = F <= Flevel
        pct[i] = pbc_largest_cluster_frac(mask, struct)
        if F_star is None and percolates(mask, struct):
            F_star = float(Flevel)
    occ = float((rho > 0).mean() * 100.0)
    print(f"[{label}] grid {rho.shape}  rho_max {rho_max:.4f}  occupied "
          f"{occ:.1f}%  ->  percolation barrier F* = "
          f"{F_star if F_star is not None else float('nan'):.3f} eV")
    return pct, F_star


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cube", action="append", required=True,
                    help="path:label  (repeat for each composition)")
    ap.add_argument("--T", type=float, default=600.0, help="AIMD temperature (K)")
    ap.add_argument("--Fmax", type=float, default=0.30, help="max PMF level (eV)")
    ap.add_argument("--dF", type=float, default=0.005, help="PMF sweep step (eV)")
    ap.add_argument("--out", default="percolation.csv")
    ap.add_argument("--plot", default=None, help="optional PNG output")
    a = ap.parse_args()

    kT = KB * a.T
    F_grid = np.arange(a.dF, a.Fmax + 1e-9, a.dF)
    print(f"kT({a.T:.0f}K) = {kT:.4f} eV ; sweeping F in "
          f"[{a.dF:.3f},{a.Fmax:.3f}] step {a.dF:.3f}")

    cols, labels, stars = [], [], []
    for spec in a.cube:
        path, _, label = spec.partition(":")
        label = label or path
        pct, Fstar = analyse(path, label, F_grid, kT)
        cols.append(pct)
        labels.append(label)
        stars.append(Fstar)

    header = "F_eV," + ",".join(f"{l}_pct" for l in labels)
    star_note = " ; ".join(
        f"{l} F*={s:.3f}eV" if s is not None else f"{l} F*=nan"
        for l, s in zip(labels, stars))
    M = np.column_stack([F_grid] + cols)
    np.savetxt(a.out, M, delimiter=",", header=header + "\n# " + star_note,
               comments="", fmt="%.5f")
    print(f"-> {a.out}\n   thresholds: {star_note}")

    if a.plot:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        colors = ["#1f77b4", "#d62728", "#2ca02c", "#9467bd"]
        plt.figure(figsize=(6.2, 4.6))
        for j, (l, s) in enumerate(zip(labels, stars)):
            c = colors[j % len(colors)]
            plt.plot(F_grid, cols[j], "-", color=c, lw=2, label=l)
            if s is not None:
                plt.axvline(s, color=c, ls="--", lw=1.3)
                plt.annotate(f"F* = {s:.3f} eV", xy=(s, 5), xytext=(s + 0.01, 8),
                             color=c, fontsize=9)
        plt.xlabel("PMF level  F = -kT ln(rho/rho_max)  [eV]")
        plt.ylabel("largest connected Li cluster  [% of cell]")
        plt.title("Li-network percolation barrier")
        plt.legend(frameon=False)
        plt.tight_layout()
        plt.savefig(a.plot, dpi=170)
        print(f"-> {a.plot}")


if __name__ == "__main__":
    main()
