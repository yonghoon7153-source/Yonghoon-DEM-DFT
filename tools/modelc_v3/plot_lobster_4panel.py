#!/usr/bin/env python3
"""4-panel pCOHP / ICOHP plot from LOBSTER output, matching paper Fig style.

Reads COHPCAR.lobster + ICOHPLIST.lobster from a LOBSTER run on modelC_v3
V0 SCF output. Produces a 4-panel horizontal figure (P-S | S-S | Li-S | Li-Cl)
with:
  - vertical layout: E - E_F (eV) on y, -pCOHP on x
  - bonding region (+x, right side) shaded
  - antibonding region (-x, left side) shaded
  - E_F dashed horizontal line at 0
  - ICOHP value in a rounded box at bottom of each panel
  - "Antibonding" / "Bonding" italic labels

Usage:
    python3 plot_lobster_4panel.py \\
        --lobster_dir /home/ubuntu/work/runs/modelC_v3 \\
        --out_png    /home/ubuntu/work/runs/modelC_v3/V0_COHP_4panel.png
"""
import argparse
import re
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch


PANEL_CONFIG = [
    {"label": "P–S",   "color": "#3F7BB6", "match_keys": ["P", "S"],   "exclude": ["Li"]},
    {"label": "S–S",   "color": "#C44536", "match_keys": ["S", "S"],   "exclude": ["P", "Li", "Cl"]},
    {"label": "Li–S",  "color": "#3E8E41", "match_keys": ["Li", "S"],  "exclude": []},
    {"label": "Li–Cl", "color": "#E89C2B", "match_keys": ["Li", "Cl"], "exclude": []},
]


def parse_cohpcar(path: Path):
    """Parse COHPCAR.lobster: returns (E, dict of {bond_label: -pCOHP array}).

    LOBSTER COHPCAR format:
        Line 1: header
        Line 2: '# of bonds, # of energies, ...'
        Line 3 onwards: '# bond_idx: atom1[N1]-atom2[N2] distance ...' for each bond
        ...
        Energy block: each line is 'E_rel  total  total_int  bond1  bond1_int  bond2 ...'
    """
    lines = path.read_text().splitlines()
    # find header line with bond definitions
    bond_labels = []
    n_bonds = 0
    n_energies = 0
    iline = 0
    for i, line in enumerate(lines):
        if line.startswith("# of bonds") or line.startswith("#of bonds"):
            parts = line.split()
            # try various formats
            try:
                n_bonds = int(parts[3])
                n_energies = int(parts[4]) if len(parts) > 4 else 0
            except (IndexError, ValueError):
                pass
            iline = i + 1
            break
        elif re.match(r"\s*\d+\s+\d+", line) and i > 0:
            parts = line.split()
            if len(parts) >= 2:
                n_bonds = int(parts[0])
                n_energies = int(parts[1])
                iline = i + 1
                break
    # bond label lines
    for j in range(n_bonds):
        line = lines[iline + j]
        # format: 'No.idx:atom1[N1]->atom2[N2](dist)'
        # or 'No.1: Li1->S2 (2.45)'
        m = re.search(r"(?:No\.\s*)?\d+:\s*([A-Za-z]+)\d*(?:\[[^\]]+\])?\s*[-=]?>?\s*([A-Za-z]+)\d*", line)
        if m:
            a1 = re.sub(r"\d", "", m.group(1))
            a2 = re.sub(r"\d", "", m.group(2))
            bond_labels.append(f"{a1}-{a2}")
        else:
            bond_labels.append(f"bond_{j+1}")
    iline += n_bonds
    # parse energy block
    E = []
    cohp_per_bond = [[] for _ in range(n_bonds)]
    for j in range(n_energies):
        if iline + j >= len(lines):
            break
        parts = lines[iline + j].split()
        if len(parts) < 3 + 2 * n_bonds:
            continue
        E.append(float(parts[0]))
        # column layout: E, total_COHP, total_ICOHP, b1_COHP, b1_ICOHP, b2_COHP, b2_ICOHP, ...
        for b in range(n_bonds):
            cohp_per_bond[b].append(float(parts[3 + 2 * b]))
    E = np.array(E)
    # COHPCAR stores COHP. Convention: -pCOHP (bonding > 0, antibonding < 0)
    # → we plot -pCOHP, which means we need -(stored COHP).
    bonds = {bond_labels[b]: -np.array(cohp_per_bond[b]) for b in range(n_bonds)}
    return E, bonds


def parse_icohplist(path: Path):
    """Parse ICOHPLIST.lobster: returns {bond_label: ICOHP value (eV)}."""
    icohp_per_bond_idx = {}
    for line in path.read_text().splitlines():
        s = line.strip()
        if not s or s.startswith("#") or s.startswith("COHP") or s.startswith("LABEL"):
            continue
        parts = s.split()
        if len(parts) >= 7:
            try:
                idx = int(parts[0])
                a1 = re.sub(r"\d", "", parts[1])
                a2 = re.sub(r"\d", "", parts[2])
                icohp = float(parts[7]) if len(parts) > 7 else float(parts[-1])
                key = f"{a1}-{a2}"
                icohp_per_bond_idx.setdefault(key, []).append(icohp)
            except (ValueError, IndexError):
                continue
    return {k: float(np.mean(v)) for k, v in icohp_per_bond_idx.items()}


def aggregate_bond_pair(E, bonds_data, icohp_data, match_keys, exclude=None):
    """Sum -pCOHP across all bonds matching the requested element pair.
    Returns (cohp_summed, icohp_summed_value).
    """
    exclude = exclude or []
    a, b = match_keys
    # accept both A-B and B-A
    matched_labels = []
    for lbl in bonds_data:
        elems = set(lbl.split("-"))
        if {a, b}.issubset(elems) and not any(x in elems for x in exclude):
            matched_labels.append(lbl)
    if not matched_labels:
        return np.zeros_like(E), 0.0, 0
    summed = np.sum([bonds_data[lbl] for lbl in matched_labels], axis=0)
    # ICOHP is sum (extensive) — average per bond × count is what we want
    icohp_total = 0.0
    icohp_per_bond_avg = None
    bond_key = f"{a}-{b}" if f"{a}-{b}" in icohp_data else f"{b}-{a}"
    if bond_key in icohp_data:
        icohp_per_bond_avg = icohp_data[bond_key]
    if icohp_per_bond_avg is not None:
        icohp_total = icohp_per_bond_avg * len(matched_labels)
        # use the per-bond average for the figure label (paper convention varies;
        # show average per bond — most papers report per-bond ICOHP)
        icohp_summed = icohp_per_bond_avg
    else:
        icohp_summed = 0.0
    return summed, icohp_summed, len(matched_labels)


def plot_panel(ax, E, cohp, color, label, icohp_value, fermi_ref=0.0,
                xlim=None, ylim=(-12, 6)):
    """Draw one COHP panel — paper style."""
    # shade left half (antibonding) and right half (bonding) lightly
    if xlim is None:
        xmax = max(abs(cohp).max() * 1.15, 1.0)
        xlim = (-xmax, xmax)

    # filled curve on right (bonding region of -pCOHP)
    bonding_x = np.where(cohp > 0, cohp, 0)
    antibond_x = np.where(cohp < 0, cohp, 0)
    ax.fill_betweenx(E - fermi_ref, 0, bonding_x, color=color, alpha=0.55, lw=0)
    ax.fill_betweenx(E - fermi_ref, 0, antibond_x, color=color, alpha=0.55, lw=0)
    # outline
    ax.plot(cohp, E - fermi_ref, '-', color=color, lw=1.0)

    # zero vertical line
    ax.axvline(0, color='k', lw=0.7)
    # Fermi horizontal
    ax.axhline(0, color='#666', linestyle='--', lw=0.8)

    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    ax.set_xlabel(r"$-$pCOHP", fontsize=12)
    ax.tick_params(labelsize=10)

    # Antibonding (top-left) and Bonding (bottom-right) text
    ax.text(xlim[0] + (xlim[1] - xlim[0]) * 0.08,
            ylim[1] - (ylim[1] - ylim[0]) * 0.10,
            "Antibonding", fontsize=10, fontstyle='italic', color='#999', ha='left')
    ax.text(xlim[1] - (xlim[1] - xlim[0]) * 0.08,
            ylim[0] + (ylim[1] - ylim[0]) * 0.42,
            "Bonding", fontsize=10, fontstyle='italic', color='#999', ha='right')
    # E_F label
    ax.text(xlim[1] - (xlim[1] - xlim[0]) * 0.05, 0.1,
            r"$E_F$", fontsize=10, color='#666', ha='right', va='bottom')

    # Legend (label in top-right)
    leg_text = label
    ax.text(xlim[1] - (xlim[1] - xlim[0]) * 0.05, ylim[1] - (ylim[1] - ylim[0]) * 0.04,
            leg_text, fontsize=12, fontweight='bold',
            ha='right', va='top', bbox=dict(facecolor=color, alpha=0.18,
                                              edgecolor='none', boxstyle='round,pad=0.3'))

    # ICOHP box at bottom
    icohp_str = f"ICOHP = {icohp_value:.3f} eV"
    ax.text(0, ylim[0] + (ylim[1] - ylim[0]) * 0.04, icohp_str,
            ha='center', va='bottom', fontsize=11, fontweight='bold',
            bbox=dict(boxstyle="round,pad=0.4", facecolor='white',
                       edgecolor='#666', lw=0.8))

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lobster_dir", required=True,
                    help="dir containing COHPCAR.lobster + ICOHPLIST.lobster")
    ap.add_argument("--out_png", required=True)
    ap.add_argument("--ylim", type=float, nargs=2, default=[-12, 6])
    args = ap.parse_args()

    work = Path(args.lobster_dir)
    cohp_path = work / "COHPCAR.lobster"
    icohp_path = work / "ICOHPLIST.lobster"
    if not cohp_path.exists() or not icohp_path.exists():
        raise SystemExit(f"missing LOBSTER files in {work}")

    E, bonds = parse_cohpcar(cohp_path)
    icohp = parse_icohplist(icohp_path)
    print(f"Parsed {len(bonds)} bond entries × {len(E)} energy points")
    print(f"ICOHP averages per element pair:")
    for k, v in sorted(icohp.items()):
        print(f"  {k}: {v:.3f} eV")

    fig, axes = plt.subplots(1, 4, figsize=(16, 6), sharey=True)
    for ax, cfg in zip(axes, PANEL_CONFIG):
        cohp_sum, icohp_per_bond, nb = aggregate_bond_pair(
            E, bonds, icohp, cfg["match_keys"], cfg["exclude"])
        plot_panel(ax, E, cohp_sum, cfg["color"], cfg["label"],
                    icohp_per_bond, ylim=tuple(args.ylim))
        if nb == 0:
            ax.text(0.5, 0.5, f"no {cfg['label']} bonds", transform=ax.transAxes,
                    ha='center', color='#999', fontsize=12)
    axes[0].set_ylabel(r"$E - E_F$  (eV)", fontsize=12)

    # subplot letter labels
    for letter, ax in zip("abcd", axes):
        ax.text(-0.10, 1.02, letter, transform=ax.transAxes,
                fontsize=16, fontweight='bold', ha='right', va='bottom')

    plt.tight_layout()
    plt.savefig(args.out_png, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"\n→ {args.out_png}")


if __name__ == "__main__":
    main()
