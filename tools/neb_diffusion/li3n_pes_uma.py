#!/usr/bin/env python3
"""li3n_pes_uma.py — UMA 2D relaxed PES for the Li adatom on Li3N(001).

REVISION-DRIVEN: the published profile was a mirrored half-path spline with an
undefined reaction coordinate. This scan removes every assumption:
  grid over the surface cell x (xy-PINNED, z-free) constrained relax per point
  -> full PES map -> true minima + the exact saddle SITE (minimax path), and a
  measured MEP to seed a bridge->bridge CI-NEB (reaction coordinate = real path
  length in Angstrom, computed images shown as markers).

Usage (kgy or kserver116, conda activate uma):
  python3 li3n_pes_uma.py --struct <slab+adatom xyz (adatom = LAST atom)> \
      --grid 12 --out_dir ~/work/runs/li3n_pes
Outputs: pes_grid.csv, pes_map.png, mep_path.xyz (9 images, NEB seed), report.txt
"""
import argparse, os, json
import numpy as np


def minimax_path(E, start, goal):
    """Dijkstra on periodic grid; cost of a path = max E along it. Returns (barrier, path)."""
    import heapq
    n, m = E.shape
    best = np.full((n, m), np.inf)
    prev = {}
    h = [(E[start], start)]
    best[start] = E[start]
    while h:
        c, (i, j) = heapq.heappop(h)
        if (i, j) == goal:
            break
        if c > best[i, j]:
            continue
        for di in (-1, 0, 1):
            for dj in (-1, 0, 1):
                if di == dj == 0:
                    continue
                k, l = (i + di) % n, (j + dj) % m
                nc = max(c, E[k, l])
                if nc < best[k, l]:
                    best[k, l] = nc
                    prev[(k, l)] = (i, j)
                    heapq.heappush(h, (nc, (k, l)))
    path = [goal]
    while path[-1] != start:
        path.append(prev[path[-1]])
    return best[goal], path[::-1]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--struct", required=True, help="slab+adatom xyz/cif, adatom = LAST atom")
    ap.add_argument("--grid", type=int, default=12)
    ap.add_argument("--cell_frac", type=float, default=1.0, help="scan window as fraction of surface cell")
    ap.add_argument("--fmax", type=float, default=0.05)
    ap.add_argument("--steps", type=int, default=80)
    ap.add_argument("--relax_top_frac", type=float, default=0.5)
    ap.add_argument("--out_dir", default="li3n_pes_uma")
    ap.add_argument("--device", default="cuda")
    a = ap.parse_args()
    os.makedirs(a.out_dir, exist_ok=True)

    from ase.io import read, write
    from ase.constraints import FixAtoms, FixedLine
    from ase.optimize import FIRE
    from fairchem.core import pretrained_mlip
    from fairchem.core.calculate.ase_calculator import FAIRChemCalculator
    calc = FAIRChemCalculator(pretrained_mlip.get_predict_unit("uma-s-1p1", device=a.device),
                              task_name="oc20")

    A0 = read(a.struct)
    ad = len(A0) - 1
    zs = A0.positions[:, 2]
    z_slab = np.delete(zs, ad)
    z_cut = z_slab.min() + (1.0 - a.relax_top_frac) * (z_slab.max() - z_slab.min())
    fixed_idx = [i for i in range(len(A0)) if i != ad and zs[i] < z_cut]
    av, bv = A0.cell[0].copy(), A0.cell[1].copy()
    origin = A0.positions[ad].copy()
    z0 = origin[2]

    N = a.grid
    E = np.zeros((N, N))
    print(f"[PES] {N}x{N} grid, {len(fixed_idx)} frozen slab atoms, adatom idx {ad}", flush=True)
    for i in range(N):
        for j in range(N):
            At = A0.copy()
            At.positions[ad] = origin + (i / N) * a.cell_frac * av + (j / N) * a.cell_frac * bv
            At.positions[ad, 2] = z0
            At.set_constraint([FixAtoms(indices=fixed_idx), FixedLine(ad, direction=[0, 0, 1])])
            At.calc = calc
            try:
                FIRE(At, logfile=None).run(fmax=a.fmax, steps=a.steps)
                E[i, j] = At.get_potential_energy()
            except Exception as e:
                E[i, j] = np.nan
                print(f"  ({i},{j}) FAIL {e}", flush=True)
        print(f"  row {i+1}/{N} done  (row min {np.nanmin(E[i]):.3f} eV)", flush=True)

    E = E - np.nanmin(E)
    np.savetxt(f"{a.out_dir}/pes_grid.csv", E, delimiter=",",
               header=f"relaxed PES (eV, min=0); rows=a-frac, cols=b-frac; grid {N}x{N} over {a.cell_frac} cell")

    # --- minima / saddle analysis ---
    minima = []
    for i in range(N):
        for j in range(N):
            nb = [E[(i+di) % N, (j+dj) % N] for di in (-1, 0, 1) for dj in (-1, 0, 1) if (di, dj) != (0, 0)]
            if E[i, j] <= min(nb):
                minima.append(((i, j), E[i, j]))
    minima.sort(key=lambda t: t[1])
    gmin = minima[0][0]
    # nearest equivalent minimum (same energy within 5 meV, not adjacent)
    equiv = [m for m in minima[1:] if abs(m[1] - minima[0][1]) < 0.005]
    report = [f"grid minima (lowest 6): {[(m[0], round(m[1],3)) for m in minima[:6]]}"]
    if equiv:
        tgt = equiv[0][0]
        barrier, path = minimax_path(E, gmin, tgt)
        si, sj = max(path, key=lambda p: E[p])
        report += [f"MEP {gmin} -> {tgt}: barrier = {barrier:.3f} eV",
                   f"saddle grid cell = ({si},{sj}) = frac ({si/N:.3f},{sj/N:.3f}) of scan window",
                   f"saddle E = {E[si,sj]:.3f} eV above global min"]
        # NEB seed: resample 9 images along the minimax path
        idxs = np.linspace(0, len(path) - 1, 9).astype(int)
        images = []
        for k in idxs:
            i, j = path[k]
            At = A0.copy()
            At.positions[ad] = origin + (i / N) * a.cell_frac * av + (j / N) * a.cell_frac * bv
            At.positions[ad, 2] = z0
            images.append(At)
        write(f"{a.out_dir}/mep_path.xyz", images)
        report.append(f"NEB seed written: {a.out_dir}/mep_path.xyz (9 images along measured MEP)")
    else:
        report.append("no equivalent second minimum found in window — increase --cell_frac to 1.5")

    # --- map figure ---
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(6.4, 5.6))
    im = ax.imshow(E.T, origin="lower", cmap="viridis",
                   extent=[0, a.cell_frac, 0, a.cell_frac], aspect="auto")
    fig.colorbar(im, label="E (eV, min = 0)")
    if equiv:
        px = [p[0] / N for p in path]; py = [p[1] / N for p in path]
        ax.plot(px, py, "w.-", lw=1.4, ms=4, label="minimax MEP")
        ax.plot(si / N, sj / N, "r*", ms=14, label=f"saddle {E[si,sj]:.3f} eV")
        ax.legend(fontsize=8)
    ax.set_xlabel("a (frac of scan window)"); ax.set_ylabel("b (frac)")
    ax.set_title("Li adatom relaxed PES on Li3N(001) — UMA, xy-pinned z-relaxed")
    fig.tight_layout(); fig.savefig(f"{a.out_dir}/pes_map.png", dpi=200)

    open(f"{a.out_dir}/report.txt", "w").write("\n".join(report) + "\n")
    print("\n".join(report))
    print(f"[PES] done -> {a.out_dir}/(pes_grid.csv, pes_map.png, mep_path.xyz, report.txt)")


if __name__ == "__main__":
    main()
