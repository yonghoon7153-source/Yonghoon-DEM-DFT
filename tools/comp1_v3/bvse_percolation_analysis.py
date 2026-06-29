#!/usr/bin/env python3
"""Percolation-barrier analysis + figures from a precomputed BVSE map (.npy).

Feed it the 3D BVSE grid (compute_bvse_map.py output) and the cif (for the cell
-> Angstrom scaling). It finds the Li migration barrier as the LOWEST BVSE
threshold at which the sub-threshold region PERCOLATES (connects through a full
period of the cell along some axis), measured above the global BVSE minimum.

  python3 bvse_percolation_analysis.py --npy V0_bvse_map.npy \
      --cif db/structures/b2o3_relaxV0.cif --prefix b2o3 --outdir docs/figures/cascade

Outputs: <prefix>_bvse_percolation.png, <prefix>_bvse_channels.png,
         <prefix>_bvse_percolation.csv, <prefix>_bvse_percolation.json
"""
import argparse, json, re, math
from pathlib import Path
import numpy as np
from scipy import ndimage
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def cell_from_cif(fn):
    t = open(fn).read()
    g = lambda k: float(re.search(k + r"\s+([\d.]+)", t).group(1))
    a, b, c = g("_cell_length_a"), g("_cell_length_b"), g("_cell_length_c")
    al, be, ga = (math.radians(g("_cell_angle_" + x)) for x in ("alpha", "beta", "gamma"))
    return (a, b, c), (al, be, ga)


def percolates(mask, axis):
    """True if {mask} connects through one full period along `axis` (PBC)."""
    N = mask.shape[axis]
    big = np.concatenate([mask, mask], axis=axis)      # 2x tile along axis
    lbl, n = ndimage.label(big)
    for k in range(1, n + 1):
        idx = np.where(lbl == k)[axis]
        if idx.size and (idx.max() - idx.min()) >= N:
            return True
    return False


def perc_any(mask):
    return any(percolates(mask, ax) for ax in range(3))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--npy", required=True, help="3D BVSE map (.npy)")
    ap.add_argument("--cif", default="db/structures/b2o3_relaxV0.cif")
    ap.add_argument("--prefix", default="b2o3")
    ap.add_argument("--outdir", default="docs/figures/cascade")
    ap.add_argument("--n_levels", type=int, default=80)
    args = ap.parse_args()
    out = Path(args.outdir); out.mkdir(parents=True, exist_ok=True)

    bvse = np.load(args.npy)
    (a, b, c), _ = cell_from_cif(args.cif)
    L = np.array([a, b, c]); nx, ny, nz = bvse.shape
    vox = L / np.array([nx, ny, nz])
    Emin = float(bvse.min())
    print(f"map {bvse.shape}  |a||b||c|={a:.2f},{b:.2f},{c:.2f} A  "
          f"voxel~{vox.min():.3f} A  BVSE min={Emin:.4f}")

    # threshold sweep -> percolation onset + per-axis + low-region fraction
    hi = float(np.percentile(bvse, 70))
    levels = np.linspace(Emin, hi, args.n_levels)
    rows, Eperc, axperc = [], None, None
    for E in levels:
        m = bvse <= E
        pax = [percolates(m, ax) for ax in range(3)]
        frac = float(m.mean())
        rows.append((float(E), float(E - Emin), frac, *pax, any(pax)))
        if Eperc is None and any(pax):
            Eperc = float(E); axperc = [i for i, p in enumerate(pax) if p]
    barrier = (Eperc - Emin) if Eperc is not None else None
    axname = ["a", "b", "c"]
    print(f"PERCOLATION onset E={Eperc}  barrier(above min)={barrier}  "
          f"axis={[axname[i] for i in (axperc or [])]}")

    # ---- CSV ----
    csv = out / f"{args.prefix}_bvse_percolation.csv"
    with open(csv, "w") as f:
        f.write("BVSE_level,BVSE_above_min,low_region_fraction,perc_a,perc_b,perc_c,percolates\n")
        for r in rows:
            f.write("%.5f,%.5f,%.5f,%d,%d,%d,%d\n" %
                    (r[0], r[1], r[2], r[3], r[4], r[5], r[6]))

    summ = {
        "npy": args.npy, "grid": [nx, ny, nz],
        "cell_A": [a, b, c], "voxel_A": [float(x) for x in vox],
        "bvse_min": Emin, "perc_onset_level": Eperc,
        "Li_migration_barrier_BVSE_above_min": barrier,
        "perc_axes": [axname[i] for i in (axperc or [])],
        "units": "BVSE valence^2 (empirical) — calibrate vs reference, not absolute eV",
    }
    (out / f"{args.prefix}_bvse_percolation.json").write_text(json.dumps(summ, indent=2))

    # ---- FIG 1: percolation curve ----
    arr = np.array([(r[1], r[2], r[6]) for r in rows])  # above_min, frac, perc
    fig, ax1 = plt.subplots(figsize=(7, 4.6))
    ax1.plot(arr[:, 0], arr[:, 1] * 100, "-", color="#2b6cb0", lw=2,
             label="low-BVSE region fraction")
    ax1.set_xlabel("BVSE above global min  (valence$^2$)")
    ax1.set_ylabel("sub-threshold volume fraction (%)", color="#2b6cb0")
    ax1.tick_params(axis="y", labelcolor="#2b6cb0")
    if barrier is not None:
        ax1.axvline(barrier, color="#c53030", ls="--", lw=1.8)
        ax1.annotate(f"percolation barrier\n≈ {barrier:.3f} (val$^2$), axis {','.join(summ['perc_axes'])}",
                     xy=(barrier, ax1.get_ylim()[1]*0.5),
                     xytext=(barrier + (arr[:,0].max()-barrier)*0.18, ax1.get_ylim()[1]*0.62),
                     color="#c53030", fontsize=9,
                     arrowprops=dict(arrowstyle="->", color="#c53030"))
    onset = arr[:, 2].astype(bool)
    ax1.fill_between(arr[:, 0], 0, ax1.get_ylim()[1], where=onset,
                     color="#9ae6b4", alpha=0.25, label="percolating (connected)")
    ax1.set_title(f"{args.prefix}: BVSE percolation — Li channel connects at the dashed line")
    ax1.legend(loc="upper left", fontsize=8); ax1.grid(alpha=0.3)
    fig.tight_layout(); fig.savefig(out / f"{args.prefix}_bvse_percolation.png", dpi=160)

    # ---- FIG 2: BVSE channel projections (min along each axis) ----
    fig, axs = plt.subplots(1, 3, figsize=(13, 4.2))
    projs = [(bvse.min(axis=0), "b", "c", "min along a"),
             (bvse.min(axis=1), "a", "c", "min along b"),
             (bvse.min(axis=2), "a", "b", "min along c")]
    for ax, (P, xl, yl, ttl) in zip(axs, projs):
        im = ax.imshow(P.T, origin="lower", aspect="auto", cmap="viridis_r",
                       vmin=Emin, vmax=float(np.percentile(bvse, 50)))
        ax.set_title(f"{ttl}\n(dark = low BVSE = Li channel)", fontsize=9)
        ax.set_xlabel(xl); ax.set_ylabel(yl)
        plt.colorbar(im, ax=ax, fraction=0.046, label="BVSE (val$^2$)")
    fig.suptitle(f"{args.prefix}: BVSE landscape — connected dark regions = Li migration network",
                 fontsize=11)
    fig.tight_layout(); fig.savefig(out / f"{args.prefix}_bvse_channels.png", dpi=150)

    print(f"-> {csv}")
    print(f"-> {out}/{args.prefix}_bvse_percolation.png")
    print(f"-> {out}/{args.prefix}_bvse_channels.png")
    print(f"-> {out}/{args.prefix}_bvse_percolation.json")


if __name__ == "__main__":
    main()
