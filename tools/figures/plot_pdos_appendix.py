#!/usr/bin/env python3
"""Appendix-style element-resolved PDOS figure (E - E_VBM axis), one system per figure.

Reproduces the legacy appendix look (stacked Li/P/S/Cl fills + total DOS, yellow gap
band, VBM/CBM dashed lines) but with the CURRENT canonical gap detection — the same
algorithm as tools/modelc_v3/plot_dos.py (low-DOS run straddling EF, else longest run),
which reproduces the V0_regen values: comp1 gap 1.76 (VBM 2.48 / CBM 4.24),
modelc gap 1.82 (VBM 2.72 / CBM 4.54).

Usage (WSL, on the V100 backup):
  python3 tools/figures/plot_pdos_appendix.py \
      --dir "/mnt/d/v100백업/runs/comp1_v3/v3_post/k444_props" --prefix V0 \
      --label "LPSCl (comp1) — Li$_6$PS$_5$Cl" --out comp1_pdos_appendix.png

  python3 tools/figures/plot_pdos_appendix.py \
      --dir "/mnt/d/v100백업/runs/modelC_v3" --prefix V0 \
      --label "LPSCl$_{1.6}$ (modelc) — Li$_{5.4}$PS$_{4.4}$Cl$_{1.6}$" \
      --out modelc_pdos_appendix.png

Check the printed VBM/CBM/gap before using: comp1 must give 2.48/4.24/1.76,
modelc 2.72/4.54/1.82 (else wrong data dir / old archive).
"""
import argparse
import re
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt

ELEM_COLOR = {
    "Li": "tab:blue",
    "P":  "tab:orange",
    "S":  "tab:green",
    "Cl": "tab:purple",
    "Br": "tab:brown",
    "O":  "tab:red",
    "Nd": "tab:cyan",
}
ELEM_ORDER = ["Li", "P", "S", "Cl", "Br", "O", "Nd"]


def read_total_dos(dos_dat: Path):
    EF = None
    with open(dos_dat) as f:
        m = re.search(r"EFermi\s*=\s*([\-\d.]+)\s*eV", f.readline())
        if m:
            EF = float(m.group(1))
    data = np.loadtxt(dos_dat, comments="#")
    return data[:, 0], data[:, 1], EF


def read_pdos_files(pdos_dir: Path, prefix: str):
    pat = re.compile(rf"{re.escape(prefix)}_pdos\.pdos_atm#(\d+)\(([A-Za-z]+)\)_wfc#(\d+)\(([a-z])\)$")
    per_elem = {}
    E_ref = None
    for fp in sorted(pdos_dir.iterdir()):
        m = pat.match(fp.name)
        if not m:
            continue
        elem = m.group(2)
        data = np.loadtxt(fp, comments="#")
        if E_ref is None:
            E_ref = data[:, 0]
        per_elem.setdefault(elem, np.zeros(len(data)))
        per_elem[elem] += data[:, 1]
    return E_ref, per_elem


def find_gap(E, DOS, EF, e_min=-3.0, dos_thresh=0.5):
    """Same algorithm as tools/modelc_v3/plot_dos.py (canonical / regen-consistent)."""
    mask = E >= e_min
    Em, Dm = E[mask], DOS[mask]
    low = Dm < dos_thresh
    runs, i = [], 0
    while i < len(low):
        if low[i]:
            j = i
            while j < len(low) and low[j]:
                j += 1
            runs.append((i, j - i))
            i = j
        else:
            i += 1
    runs = [r for r in runs if r[1] >= 3]
    if not runs:
        raise SystemExit("no gap found — check data / thresholds")
    chosen = None
    if EF is not None:
        for (s, n) in runs:
            if Em[s] <= EF <= Em[min(s + n - 1, len(Em) - 1)]:
                chosen = (s, n)
                break
    if chosen is None:
        chosen = max(runs, key=lambda r: r[1])
    s, n = chosen
    vbm = float(Em[max(s - 1, 0)])
    cbm = float(Em[min(s + n, len(Em) - 1)])
    return vbm, cbm, cbm - vbm


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", required=True)
    ap.add_argument("--prefix", default="V0")
    ap.add_argument("--label", default="")
    ap.add_argument("--out", default=None)
    ap.add_argument("--xlim", type=float, nargs=2, default=[-15, 7],
                    help="x range in E - E_VBM (eV)")
    ap.add_argument("--e_min", type=float, default=-3.0)
    ap.add_argument("--dos_thresh", type=float, default=0.5)
    args = ap.parse_args()

    d = Path(args.dir)
    E, DOS, EF = read_total_dos(d / f"{args.prefix}_dos.dat")
    E_p, per_elem = read_pdos_files(d, args.prefix)
    vbm, cbm, gap = find_gap(E, DOS, EF, e_min=args.e_min, dos_thresh=args.dos_thresh)
    print(f"EF={EF:.3f}  VBM={vbm:.2f}  CBM={cbm:.2f}  gap={gap:.2f} eV")

    x = E - vbm
    x_p = E_p - vbm
    fig, ax = plt.subplots(figsize=(11, 5.5))
    ax.plot(x, DOS, color="black", lw=1.8, label="Total DOS", zorder=5)
    for el in ELEM_ORDER:
        if el in per_elem:
            ax.fill_between(x_p, 0, per_elem[el], color=ELEM_COLOR[el],
                            alpha=0.45, label=el)
            ax.plot(x_p, per_elem[el], color=ELEM_COLOR[el], lw=0.8, alpha=0.8)
    ax.axvline(0, color="blue", ls="--", lw=1.4, label=f"VBM = {vbm:.2f} eV")
    ax.axvline(gap, color="red", ls="--", lw=1.4, label=f"CBM = {cbm:.2f} eV")
    ax.axvspan(0, gap, color="lightyellow", alpha=0.8, label=f"gap = {gap:.2f} eV")
    ax.set_xlim(*args.xlim)
    ax.set_ylim(bottom=0)
    ax.set_xlabel(r"$E - E_{VBM}$ (eV)", fontsize=14)
    ax.set_ylabel("DOS (states/eV)", fontsize=14)
    ax.tick_params(labelsize=12)
    title = f"{args.label}   band gap = {gap:.2f} eV" if args.label else f"band gap = {gap:.2f} eV"
    ax.set_title(title, fontsize=15)
    ax.legend(loc="upper right", fontsize=11, framealpha=0.95)
    ax.grid(alpha=0.3)
    plt.tight_layout()
    out = args.out or str(d / f"{args.prefix}_pdos_appendix.png")
    plt.savefig(out, dpi=300, facecolor="white", bbox_inches="tight")
    print(f"→ {out}")


if __name__ == "__main__":
    main()
