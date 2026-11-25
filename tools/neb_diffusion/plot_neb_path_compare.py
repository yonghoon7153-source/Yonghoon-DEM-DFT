#!/usr/bin/env python3
"""NEB diffusion path E-vs-reaction-coord comparison (paper Figure h alt).

Designed for the case where ABSOLUTE barrier values depend on DFT setup
(functional, pseudo, NEB protocol), so the paper-strong message is:

  "Same DFT protocol → Li3N vs LiC6 (and any other phase) on one axis."

Reads dft_neb_results.json files (written by run_dft_neb.sh) or accepts
raw image-energy lists via CLI. Plots each system as a smooth curve over a
normalized reaction coordinate [0, 1], with markers at the 7 NEB images and
annotated effective barriers.

Usage (JSON):
    python3 plot_neb_path_compare.py \\
        --systems li3n=/path/.../li3n_dft_neb_results.json \\
                  lic6=/path/.../lic6_dft_neb_results.json \\
        --labels  'Li$_3$N (001)' 'LiC$_6$ (0001)' \\
        --out output/neb_path_compare.png

Usage (raw energies, eV relative to image 0):
    python3 plot_neb_path_compare.py \\
        --raw li3n='0,-0.005,-0.008,-0.010,-0.005,0.039,0.000' \\
              lic6='0,0.06,0.13,0.20,0.241,0.18,0.003' \\
        --labels 'Li$_3$N (001)' 'LiC$_6$ (0001)' \\
        --out output/neb_path_compare.png
"""
import argparse
import json
import sys
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt


# Default palette (paper-friendly, color-blind-safe-ish)
DEFAULT_COLORS = [
    "#3B5BA0",  # deep blue   — Li3N
    "#5A5A5A",  # dark gray   — LiC6 (anode-free baseline)
    "#C44536",  # red         — extras
    "#3E8E41",  # green
    "#E89C2B",  # amber
]


def _load_rel_energies(spec):
    """spec = 'key=value'  where value is .json path or comma-eV string."""
    if "=" not in spec:
        raise SystemExit(f"--systems / --raw entry must be key=value: {spec}")
    key, val = spec.split("=", 1)
    if val.endswith(".json"):
        with open(val) as f:
            d = json.load(f)
        rel = d.get("rel_energies_eV")
        if rel is None:
            raise SystemExit(f"{val}: no 'rel_energies_eV' key")
        return key, [float(x) for x in rel]
    # raw comma-separated
    return key, [float(x) for x in val.split(",")]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--systems", nargs="+", default=[],
                    help="key=path-to-dft_neb_results.json (one or more)")
    ap.add_argument("--raw", nargs="+", default=[],
                    help="key='e0,e1,e2,...' raw rel-energies in eV (image 0=0)")
    ap.add_argument("--labels", nargs="+", default=None,
                    help="display labels for systems (in same order)")
    ap.add_argument("--colors", nargs="+", default=None)
    ap.add_argument("--out", required=True)
    ap.add_argument("--title", default=None)
    ap.add_argument("--xlabel", default="Reaction coordinate")
    ap.add_argument("--ylabel", default="Relative energy (eV)")
    ap.add_argument("--figsize", type=float, nargs=2, default=[7.0, 4.8])
    ap.add_argument("--dpi", type=int, default=300)
    ap.add_argument("--smooth", action="store_true", default=True,
                    help="cubic spline interpolation between images (default)")
    ap.add_argument("--no_smooth", dest="smooth", action="store_false")
    ap.add_argument("--annotate_barrier", action="store_true", default=True)
    args = ap.parse_args()

    entries = []
    # NOTE: --systems and --raw are honored in the order they appear on the
    # command line by concatenating, but for backward-compat with previous
    # behavior we issue a warning when both are used (mixed order is fragile).
    if args.systems and args.raw:
        print("[plot_neb_path_compare] WARNING: mixing --systems and --raw "
              "fixes processing order (systems first, then raw). For correct "
              "label alignment, prefer one mode only.", file=sys.stderr)
    for s in args.systems:
        entries.append(_load_rel_energies(s))
    for s in args.raw:
        entries.append(_load_rel_energies(s))
    if not entries:
        raise SystemExit("No data: provide --systems or --raw")

    labels = args.labels if args.labels else [k for k, _ in entries]
    if len(labels) != len(entries):
        raise SystemExit("--labels count must match # systems")
    colors = args.colors if args.colors else DEFAULT_COLORS[:len(entries)]

    fig, ax = plt.subplots(figsize=tuple(args.figsize))

    for (key, rel), lbl, col in zip(entries, labels, colors):
        n = len(rel)
        x = np.linspace(0, 1, n)
        rel = np.array(rel)

        # Smooth curve
        if args.smooth and n >= 4:
            from scipy.interpolate import CubicSpline
            cs = CubicSpline(x, rel)
            xs = np.linspace(0, 1, 200)
            ys = cs(xs)
            ax.plot(xs, ys, '-', color=col, lw=2.2, zorder=3)
        else:
            ax.plot(x, rel, '-', color=col, lw=2.2, zorder=3)

        # Image markers
        ax.plot(x, rel, 'o', mfc=col, mec='k', mew=0.8, ms=8, zorder=4)

        # Barrier annotation
        ts_idx = int(np.argmax(rel))
        bridge_idx = int(np.argmin(rel))
        ts_E = rel[ts_idx]
        bridge_E = rel[bridge_idx] if rel[bridge_idx] < -1e-3 else 0.0
        eff_barrier = ts_E - bridge_E
        endpoint_barrier = ts_E  # vs image 0

        label_full = f"{lbl}  (Ea = {eff_barrier*1000:.0f} meV)"
        # update legend entry by re-plotting an invisible line w/ label
        ax.plot([], [], '-', color=col, lw=2.2, label=label_full)

        if args.annotate_barrier:
            # Mark TS
            ax.annotate("", xy=(x[ts_idx], ts_E),
                        xytext=(x[ts_idx], bridge_E),
                        arrowprops=dict(arrowstyle="<->", color=col, lw=1.2))
            ax.text(x[ts_idx] + 0.02, (ts_E + bridge_E) / 2,
                    f"{eff_barrier*1000:.0f} meV",
                    color=col, fontsize=9, va='center')

    # Zero reference line
    ax.axhline(0, color='#999', lw=0.8, linestyle=':', zorder=1)

    ax.set_xlabel(args.xlabel, fontsize=12)
    ax.set_ylabel(args.ylabel, fontsize=12)
    if args.title:
        ax.set_title(args.title, fontsize=12)
    ax.set_xlim(-0.02, 1.02)
    ax.grid(axis='y', linestyle='--', alpha=0.3, zorder=0)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.legend(loc='best', fontsize=10, frameon=False)

    out = Path(args.out); out.parent.mkdir(parents=True, exist_ok=True)
    plt.tight_layout()
    plt.savefig(out, dpi=args.dpi, bbox_inches='tight', facecolor='white')
    print(f"\n→ {out}")


if __name__ == "__main__":
    main()
