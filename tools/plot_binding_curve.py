#!/usr/bin/env python3
"""
Binding energy curve: E(d) vs interface gap.

Analogous to WSe2/MoSe2 adhesion curves (Figure from user advisor).
For each composition, sweeps the SE-NCM gap d from d_min to d_max
with the SE slab xy-shifted to a representative registry.

Inputs: xyz files of relaxed v5 interfaces (on V100/KISTI).
Output:
    - per-comp E(d) curves (one JSON per comp)
    - combined plot: 5 comps overlaid

Usage (on V100/KISTI with UMA env):
    python tools/plot_binding_curve.py comp3_v5xy_s45.xyz
    python tools/plot_binding_curve.py comp*_v5xy_s*.xyz --combined

The equilibrium d and well depth (= Wad) emerge from the minimum.
"""
import argparse
import json
from pathlib import Path

import numpy as np


def sweep_gap(interface_xyz, n_ncm=None, d_min=1.0, d_max=8.0, n_points=30,
              device="cuda"):
    """
    Sweep z-gap between NCM and SE slabs, compute single-point E at each gap.

    Requires fairchem/ASE (run on V100/KISTI with UMA env).
    """
    from ase.io import read
    from fairchem.core import pretrained_mlip
    from fairchem.core.calculate.ase_calculator import FAIRChemCalculator

    atoms = read(interface_xyz)

    # Auto-detect NCM boundary: first P atom = SE start
    if n_ncm is None:
        for i, s in enumerate(atoms.symbols):
            if s == 'P':
                n_ncm = i
                break

    predictor = pretrained_mlip.get_predict_unit("uma-s-1p1", device=device)

    def new_calc():
        return FAIRChemCalculator(predictor, task_name="omat")

    # Current gap = SE_zmin - NCM_zmax
    pos = atoms.get_positions()
    ncm_zmax = pos[:n_ncm, 2].max()
    se_zmin_init = pos[n_ncm:, 2].min()
    d_init = se_zmin_init - ncm_zmax
    area = np.linalg.norm(
        np.cross(atoms.cell.array[0], atoms.cell.array[1])
    )

    print(f"Initial gap d0 = {d_init:.3f} Å, area = {area:.2f} Å²")
    print(f"Sweeping d = {d_min} → {d_max} Å, {n_points} points")

    # 1) Get reference E_sep at large separation (once)
    atoms_sep = atoms.copy()
    pos_sep = atoms_sep.get_positions()
    pos_sep[n_ncm:, 2] += 30.0
    atoms_sep.set_positions(pos_sep)
    cell_sep = atoms_sep.cell.array.copy()
    cell_sep[2, 2] += 30.0
    atoms_sep.set_cell(cell_sep)
    atoms_sep.calc = new_calc()
    E_sep = atoms_sep.get_potential_energy()
    print(f"E_sep (large separation) = {E_sep:.4f} eV")

    # 2) Sweep d
    ds = np.linspace(d_min, d_max, n_points)
    E_values = []

    for d in ds:
        atoms_d = atoms.copy()
        pos_d = atoms_d.get_positions()
        # Shift SE so that SE_zmin = ncm_zmax + d
        shift = (ncm_zmax + d) - pos_d[n_ncm:, 2].min()
        pos_d[n_ncm:, 2] += shift
        atoms_d.set_positions(pos_d)
        atoms_d.calc = new_calc()
        E = atoms_d.get_potential_energy()
        E_values.append(E)
        print(f"  d={d:.2f} Å  E={E:.4f} eV  ΔE_binding={(E_sep-E)*16.0218/area:+.3f} J/m²")

    E_values = np.array(E_values)
    # Binding energy (relative to separated state): positive = bound
    E_binding = (E_sep - E_values) / area * 16.0218   # J/m²
    # For Lennard-Jones style display, keep it negative (attractive)
    # E_curve = -E_binding (well shape matches user's advisor plot)

    return {
        "filename": str(interface_xyz),
        "n_ncm": int(n_ncm),
        "area_A2": float(area),
        "d_min": float(d_min),
        "d_max": float(d_max),
        "n_points": int(n_points),
        "d_values_A": ds.tolist(),
        "E_tot_eV": E_values.tolist(),
        "E_sep_eV": float(E_sep),
        "E_binding_Jm2": E_binding.tolist(),
        "d_equilibrium_A": float(ds[E_values.argmin()]),
        "E_wad_Jm2": float(E_binding.max()),
    }


def plot_curves(data_dict, outpath):
    """Plot 5 E(d) curves on same figure (WSe2-style)."""
    import matplotlib.pyplot as plt

    COLORS = {"comp3": "#4FBDFF", "comp4": "#52B788", "comp5": "#F4A261",
              "comp1": "#9B5DE5", "comp2B": "#2A9D8F"}
    MARKERS = {"comp3": "o", "comp4": "s", "comp5": "^",
               "comp1": "D", "comp2B": "v"}

    fig, ax = plt.subplots(figsize=(9, 6.5))
    for comp, data in data_dict.items():
        d = np.array(data["d_values_A"])
        E = np.array(data["E_binding_Jm2"])
        # Plot as negative (well shape, attractive) like user's plot
        ax.plot(d, -E, marker=MARKERS.get(comp, "o"), markersize=6,
                color=COLORS.get(comp, "#666666"), lw=1.6,
                markeredgecolor="#404040", markeredgewidth=0.6,
                label=f"{comp}  (Wad={data['E_wad_Jm2']:.2f} J/m²)")
        # Equilibrium marker
        d_eq = data["d_equilibrium_A"]
        ax.scatter(d_eq, -data["E_wad_Jm2"], s=200, marker="*",
                   color=COLORS.get(comp, "#666666"),
                   edgecolor="#404040", lw=1.0, zorder=5)

    ax.axhline(0, color="#404040", lw=0.8, ls="--", alpha=0.6)
    ax.set_xlabel("Interface gap d (Å)", fontsize=13)
    ax.set_ylabel(r"Adhesion energy (J/m²)  [attractive = negative]",
                  fontsize=13)
    ax.set_title("Binding energy curves — argyrodite SE / LiNiO₂",
                 fontsize=13)
    ax.legend(loc="upper right", fontsize=10, frameon=False)
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(outpath, dpi=300, bbox_inches="tight")
    print(f"✓ {outpath}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="+", help="xyz files (relaxed interfaces)")
    ap.add_argument("--d-min", type=float, default=1.0)
    ap.add_argument("--d-max", type=float, default=8.0)
    ap.add_argument("--n", type=int, default=30)
    ap.add_argument("--combined", action="store_true",
                    help="also plot all curves combined")
    ap.add_argument("--device", default="cuda")
    args = ap.parse_args()

    all_data = {}
    for f in args.files:
        path = Path(f)
        if not path.exists():
            print(f"! {f} not found")
            continue
        # Infer comp name from filename
        comp = path.stem.split("_")[0]
        data = sweep_gap(path, d_min=args.d_min, d_max=args.d_max,
                         n_points=args.n, device=args.device)
        all_data[comp] = data
        json_out = path.with_name(f"{path.stem}_binding.json")
        with open(json_out, "w") as fp:
            json.dump(data, fp, indent=2)
        print(f"  saved {json_out.name}")

    if args.combined and len(all_data) >= 2:
        plot_curves(all_data, Path("binding_curves_combined.png"))


if __name__ == "__main__":
    main()
