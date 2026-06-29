#!/usr/bin/env python3
"""Compute Bond-Valence Site Energy (BVSE) map for Li in an argyrodite.

For each grid point r in the unit cell:
  BVS(r) = Σ_{X in anions} exp( (R0_X - d(r, X)) / b )
  BVSE(r) = (BVS(r) − V_ideal)²   with V_ideal = 1.0 for Li⁺

Anions = S, Cl. R0 values from Brown's bond-valence parameter table
(softBV convention). Periodic boundary conditions handled via nearest-image.

Outputs (same convention as modelc_v3 paper run):
  - V0_bvs_map.npy   (nx, ny, nz) float64
  - V0_bvse_map.npy  (nx, ny, nz) float64
  - V0_bvse_summary.json

Usage:
    python3 compute_bvse_map.py --cif V0_init.cif --workdir . --grid 20
"""
import argparse, json
from pathlib import Path
import numpy as np
from ase.io import read


BV_PARAMS = {
    "S":  {"R0": 2.105, "b": 0.37},   # Li-S (Brown)
    "Cl": {"R0": 2.249, "b": 0.37},   # Li-Cl (Brown)
    "O":  {"R0": 1.466, "b": 0.37},   # Li-O (Brown-Altermatt) — for O-doped (B2O3) cells
}
V_IDEAL_LI = 1.0


def compute_bvs_map(atoms, grid_shape, cutoff_A=5.0):
    """Vectorized BVS map computation with full PBC."""
    cell = atoms.get_cell()
    positions = atoms.get_positions()
    symbols = atoms.get_chemical_symbols()
    # Anion list
    anion_idx = [i for i, s in enumerate(symbols) if s in BV_PARAMS]
    anion_pos = positions[anion_idx]
    anion_sym = [symbols[i] for i in anion_idx]

    nx, ny, nz = grid_shape
    # Fractional grid
    fx = np.arange(nx) / nx
    fy = np.arange(ny) / ny
    fz = np.arange(nz) / nz
    Fx, Fy, Fz = np.meshgrid(fx, fy, fz, indexing="ij")
    frac_grid = np.stack([Fx.ravel(), Fy.ravel(), Fz.ravel()], axis=1)  # (N,3)
    cart_grid = frac_grid @ np.array(cell)                              # (N,3)
    N = cart_grid.shape[0]

    bvs = np.zeros(N, dtype=np.float64)
    # For each anion, compute distance to all grid points under MIC and accumulate
    cell_arr = np.array(cell)
    inv_cell = np.linalg.inv(cell_arr)
    for ax, sym in zip(anion_pos, anion_sym):
        R0 = BV_PARAMS[sym]["R0"]
        b  = BV_PARAMS[sym]["b"]
        # delta in cartesian
        d_cart = cart_grid - ax[np.newaxis, :]
        # to fractional, MIC, back to cartesian
        d_frac = d_cart @ inv_cell
        d_frac -= np.round(d_frac)
        d_cart_mic = d_frac @ cell_arr
        d = np.linalg.norm(d_cart_mic, axis=1)
        # cutoff
        mask = d < cutoff_A
        if not np.any(mask):
            continue
        bvs[mask] += np.exp((R0 - d[mask]) / b)

    bvs_map = bvs.reshape(grid_shape)
    bvse_map = (bvs_map - V_IDEAL_LI) ** 2
    return bvs_map, bvse_map


def existing_li_bvs(atoms, grid_shape=None, cutoff_A=5.0):
    """Compute BVS at each Li position via DIRECT summation over anions
    (with PBC), not via grid sampling — avoids 0.5-Å grid-snap artifacts
    that gave spurious BVS=10+ at some Li sites in disordered structures.
    """
    cell_arr = np.array(atoms.get_cell())
    inv_cell = np.linalg.inv(cell_arr)
    symbols = atoms.get_chemical_symbols()
    positions = atoms.get_positions()
    li_idx = [i for i, s in enumerate(symbols) if s == "Li"]
    anion_idx = [i for i, s in enumerate(symbols) if s in BV_PARAMS]
    if not li_idx or not anion_idx:
        return None

    vals = []
    for i in li_idx:
        li_pos = positions[i]
        bvs_li = 0.0
        for j in anion_idx:
            d_cart = positions[j] - li_pos
            d_frac = d_cart @ inv_cell
            d_frac -= np.round(d_frac)
            d_mic = d_frac @ cell_arr
            d = np.linalg.norm(d_mic)
            if d < cutoff_A:
                R0 = BV_PARAMS[symbols[j]]["R0"]
                b  = BV_PARAMS[symbols[j]]["b"]
                bvs_li += np.exp((R0 - d) / b)
        vals.append(bvs_li)
    vals = np.array(vals)
    return {
        "mean": float(vals.mean()),
        "std":  float(vals.std()),
        "min":  float(vals.min()),
        "max":  float(vals.max()),
        "per_atom_idx": [int(i) for i in li_idx],
        "per_atom_bvs": [float(v) for v in vals],
        "_method": "direct PBC sum at exact Li position (no grid sampling)",
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cif", required=True)
    ap.add_argument("--workdir", default=".")
    ap.add_argument("--grid", type=int, default=20,
                    help="grid points per axis (default 20 = 0.05 frac res)")
    ap.add_argument("--cutoff", type=float, default=5.0,
                    help="anion cutoff for BVS summation (Å)")
    ap.add_argument("--prefix", default="V0")
    args = ap.parse_args()

    wd = Path(args.workdir); wd.mkdir(parents=True, exist_ok=True)
    atoms = read(args.cif)
    # anisotropic grid: --grid = points along the SHORTEST cell axis; longer
    # axes get proportionally more points (~uniform Å spacing). For cubic cells
    # this reduces to the old (grid,grid,grid); for elongated (e.g. c=70 Å) it
    # avoids coarse voxels along the long axis.
    _L = np.asarray(atoms.cell.lengths())
    grid_shape = tuple(int(max(8, round(args.grid * float(Lk) / float(_L.min())))) for Lk in _L)
    anions = "+".join(sorted({s for s in atoms.get_chemical_symbols() if s in BV_PARAMS}))
    print(f"System: {atoms.get_chemical_formula()}, V={atoms.get_volume():.3f} Å³")
    print(f"Grid: {grid_shape} (~{float(_L.min())/args.grid:.3f} Å/voxel), anions={anions}")

    bvs, bvse = compute_bvs_map(atoms, grid_shape, args.cutoff)
    print(f"BVS range:  [{bvs.min():.4f}, {bvs.max():.4f}], median={np.median(bvs):.4f}")
    print(f"BVSE range: [{bvse.min():.4f}, {bvse.max():.4f}]")

    li_stats = existing_li_bvs(atoms, grid_shape, args.cutoff)
    if li_stats:
        print(f"BVS at existing Li sites: mean={li_stats['mean']:.4f} "
              f"± {li_stats['std']:.4f}  [{li_stats['min']:.4f}, {li_stats['max']:.4f}]")

    # Save
    bvs_p  = wd / f"{args.prefix}_bvs_map.npy"
    bvse_p = wd / f"{args.prefix}_bvse_map.npy"
    np.save(bvs_p, bvs)
    np.save(bvse_p, bvse)

    low_thresh = bvse.min() + 0.5  # arbitrary (BVSE units: valence²)
    low_frac = float((bvse <= low_thresh).sum()) / bvse.size

    summary = {
        "grid_resolution_frac": 1.0 / args.grid,
        "grid_shape": list(grid_shape),
        "cutoff_A": args.cutoff,
        "bvs_stats": {
            "min": float(bvs.min()),
            "max": float(bvs.max()),
            "median": float(np.median(bvs)),
        },
        "li_target_bvs": V_IDEAL_LI,
        "existing_Li_bvs": li_stats,
        "low_bvse_threshold_above_min": 0.5,
        "low_bvse_channel_fraction": low_frac,
        "bv_parameters": BV_PARAMS,
        "notes": "BVSE = (BVS - 1.0)^2. Lower = easier Li site / channel.",
    }
    (wd / f"{args.prefix}_bvse_summary.json").write_text(
        json.dumps(summary, indent=2))
    print(f"\n→ {bvs_p}")
    print(f"→ {bvse_p}")
    print(f"→ {wd}/{args.prefix}_bvse_summary.json")


if __name__ == "__main__":
    main()
