#!/usr/bin/env python3
"""
Halogen-O bond count vs z-position — Choi Fig 12 analog.

Counts X-O (X = Cl, Br) bonds in z-bins at SE/NCM interface to quantify
halogen-specific interfacial bonding.

Run on V100/KISTI where the xyz files live. This script works on any
ASE-readable interface file (e.g. comp3_v5xy_s45.xyz).

Usage:
    python tools/analyze_halogen_bonds.py comp3_v5xy_s45.xyz
    python tools/analyze_halogen_bonds.py *.xyz --cutoff 3.5 --bin 0.5
    python tools/analyze_halogen_bonds.py comp3_v5xy_s45.xyz --plot

Output:
    <base>_halogen_O_profile.json  — bond counts per z-bin
    <base>_halogen_O_profile.png   — plot (if --plot)
"""
import argparse
import json
from pathlib import Path

import numpy as np


def load_xyz(path):
    """Minimal xyz reader — returns (symbols, positions as Nx3 array)."""
    with open(path) as f:
        lines = f.readlines()
    n = int(lines[0].strip())
    symbols, coords = [], []
    for line in lines[2:2 + n]:
        parts = line.split()
        symbols.append(parts[0])
        coords.append([float(parts[1]), float(parts[2]), float(parts[3])])
    return np.array(symbols), np.array(coords)


def halogen_O_profile(symbols, coords, cutoff=3.5, bin_width=0.5):
    """Count X-O bonds (X in {Cl, Br}) per z-bin.

    Returns dict with z-bins and per-halogen counts.
    """
    is_O = symbols == "O"
    is_Cl = symbols == "Cl"
    is_Br = symbols == "Br"

    if not is_O.any():
        return None

    O_pos = coords[is_O]
    z_min = coords[:, 2].min()
    z_max = coords[:, 2].max()
    bins = np.arange(z_min, z_max + bin_width, bin_width)
    centers = 0.5 * (bins[:-1] + bins[1:])

    def count_X_O_per_bin(X_pos):
        if len(X_pos) == 0:
            return np.zeros(len(centers))
        # pairwise distance X[i] - O[j]
        diff = X_pos[:, None, :] - O_pos[None, :, :]
        dist = np.linalg.norm(diff, axis=2)
        mask = dist < cutoff           # (nX, nO)
        # For each X atom, count bonds (sum over O), assign to X's z
        bond_count = mask.sum(axis=1)
        counts, _ = np.histogram(X_pos[:, 2], bins=bins, weights=bond_count)
        return counts

    Cl_counts = count_X_O_per_bin(coords[is_Cl])
    Br_counts = count_X_O_per_bin(coords[is_Br])

    return {
        "z_centers": centers.tolist(),
        "bin_width": bin_width,
        "cutoff": cutoff,
        "Cl_O_bond_count": Cl_counts.tolist(),
        "Br_O_bond_count": Br_counts.tolist(),
        "n_Cl": int(is_Cl.sum()),
        "n_Br": int(is_Br.sum()),
        "n_O": int(is_O.sum()),
    }


def plot_profile(profile, outpath):
    import matplotlib.pyplot as plt
    z = np.asarray(profile["z_centers"])
    cl = np.asarray(profile["Cl_O_bond_count"])
    br = np.asarray(profile["Br_O_bond_count"])

    fig, ax = plt.subplots(figsize=(6, 4.5))
    ax.barh(z, cl, height=profile["bin_width"] * 0.85,
            color="#52B788", edgecolor="#404040", lw=0.5,
            label=f"Cl–O  (nCl={profile['n_Cl']})")
    ax.barh(z, -br, height=profile["bin_width"] * 0.85,
            color="#E76F51", edgecolor="#404040", lw=0.5,
            label=f"Br–O  (nBr={profile['n_Br']})")
    ax.axvline(0, color="#404040", lw=0.8)
    ax.set_xlabel("Bond count", fontsize=12)
    ax.set_ylabel("z position (Å)", fontsize=12)
    ax.set_title(f"Halogen–O bond profile (cutoff {profile['cutoff']} Å)",
                 fontsize=11)
    ax.legend(frameon=False, loc="upper right", fontsize=10)
    ax.grid(axis="x", alpha=0.3)
    fig.tight_layout()
    fig.savefig(outpath, dpi=300, bbox_inches="tight")
    plt.close(fig)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="+", help="xyz files (interface structures)")
    ap.add_argument("--cutoff", type=float, default=3.5,
                    help="X-O bond cutoff in Å (default 3.5)")
    ap.add_argument("--bin", type=float, default=0.5,
                    help="z-bin width in Å (default 0.5)")
    ap.add_argument("--plot", action="store_true",
                    help="save PNG plot next to JSON")
    args = ap.parse_args()

    for f in args.files:
        path = Path(f)
        if not path.exists():
            print(f"! {f} not found")
            continue
        symbols, coords = load_xyz(path)
        profile = halogen_O_profile(symbols, coords,
                                    cutoff=args.cutoff, bin_width=args.bin)
        if profile is None:
            print(f"! {path.name}: no O atoms found (not an interface?)")
            continue
        out_json = path.with_name(path.stem + "_halogen_O_profile.json")
        with open(out_json, "w") as fp:
            json.dump(profile, fp, indent=2)
        print(f"✓ {out_json.name}  (Cl bonds sum={sum(profile['Cl_O_bond_count']):.0f}, "
              f"Br bonds sum={sum(profile['Br_O_bond_count']):.0f})")
        if args.plot:
            out_png = path.with_name(path.stem + "_halogen_O_profile.png")
            plot_profile(profile, out_png)
            print(f"  ✓ {out_png.name}")


if __name__ == "__main__":
    main()
