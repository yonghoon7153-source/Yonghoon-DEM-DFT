#!/usr/bin/env python3
"""
Li layer partitioning — Choi Fig S17 analog.

Classifies SE Li atoms into 1st/2nd/3rd interfacial layers based on
distance from the NCM O surface. Visualizes vacancy-mediated anchoring
by comparing Li5.4 (vacancy) vs Li6 (no vacancy) interfaces.

Layer definitions (mirror Choi S17 logic):
  - Li_1st : Li atoms within 3 Å of nearest NCM O
  - Li_2nd : 3 Å < distance < 6 Å
  - Li_3rd : distance >= 6 Å (bulk-like)

Usage:
    python tools/li_layer_partition.py comp1_v5xy_s45.xyz
    python tools/li_layer_partition.py *.xyz --th1 3.0 --th2 6.0

Outputs per file:
    <base>_li_layers.json   — counts + mean z per layer
"""
import argparse
import json
from pathlib import Path

import numpy as np


def load_xyz(path):
    with open(path) as f:
        lines = f.readlines()
    n = int(lines[0].strip())
    symbols, coords = [], []
    for line in lines[2:2 + n]:
        parts = line.split()
        symbols.append(parts[0])
        coords.append([float(parts[1]), float(parts[2]), float(parts[3])])
    return np.array(symbols), np.array(coords)


def partition_li(symbols, coords, th1=3.0, th2=6.0):
    """Return per-Li distance to nearest NCM O and layer assignment."""
    is_O = symbols == "O"
    is_Li = symbols == "Li"

    if not is_O.any():
        raise ValueError("No O atoms (not an interface structure)")

    O_pos = coords[is_O]
    # NCM O = lower z region (NCM is stacked first, SE on top)
    # Use top-most O layer as interface reference
    O_z_top = O_pos[:, 2].max()
    ncm_top_O = O_pos[np.abs(O_pos[:, 2] - O_z_top) < 1.5]

    # For each Li, find nearest NCM-top-O distance
    Li_pos = coords[is_Li]
    Li_idx = np.where(is_Li)[0]

    # Only consider SE Li (above NCM top)
    se_Li_mask = Li_pos[:, 2] > O_z_top - 0.5
    se_Li_pos = Li_pos[se_Li_mask]
    se_Li_idx = Li_idx[se_Li_mask]

    if len(se_Li_pos) == 0:
        return None

    # Distance matrix Li -> NCM-top-O, take min
    diff = se_Li_pos[:, None, :] - ncm_top_O[None, :, :]
    dist = np.linalg.norm(diff, axis=2).min(axis=1)

    layers = np.where(dist < th1, 1,
                      np.where(dist < th2, 2, 3))

    def stats(mask):
        if mask.sum() == 0:
            return {"n": 0, "mean_z": None, "mean_dist": None}
        return {
            "n": int(mask.sum()),
            "mean_z": float(se_Li_pos[mask, 2].mean()),
            "mean_dist": float(dist[mask].mean()),
        }

    return {
        "n_se_Li": int(len(se_Li_pos)),
        "ncm_top_O_z": float(O_z_top),
        "thresholds": {"th1": th1, "th2": th2},
        "Li_1st": stats(layers == 1),
        "Li_2nd": stats(layers == 2),
        "Li_3rd": stats(layers == 3),
        "fraction_1st": float((layers == 1).mean()),
        "fraction_2nd": float((layers == 2).mean()),
        "fraction_3rd": float((layers == 3).mean()),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="+")
    ap.add_argument("--th1", type=float, default=3.0,
                    help="Distance threshold for Li_1st (Å)")
    ap.add_argument("--th2", type=float, default=6.0,
                    help="Distance threshold for Li_2nd (Å)")
    args = ap.parse_args()

    aggregate = {}
    for f in args.files:
        path = Path(f)
        if not path.exists():
            print(f"! {f} not found")
            continue
        symbols, coords = load_xyz(path)
        result = partition_li(symbols, coords, th1=args.th1, th2=args.th2)
        if result is None:
            print(f"! {path.name}: no SE Li found")
            continue
        outp = path.with_name(path.stem + "_li_layers.json")
        with open(outp, "w") as fp:
            json.dump(result, fp, indent=2)
        aggregate[path.stem] = result
        print(f"✓ {outp.name}  "
              f"1st:{result['Li_1st']['n']} "
              f"2nd:{result['Li_2nd']['n']} "
              f"3rd:{result['Li_3rd']['n']} "
              f"(frac_1st={result['fraction_1st']:.2f})")

    if len(aggregate) > 1:
        summary = Path("li_layer_summary.json")
        with open(summary, "w") as fp:
            json.dump(aggregate, fp, indent=2)
        print(f"\n✓ {summary} (combined)")


if __name__ == "__main__":
    main()
