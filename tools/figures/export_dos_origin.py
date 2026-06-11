#!/usr/bin/env python3
"""Export comp1 + modelc total DOS to one Origin-ready CSV (+ preview PNG).

Input: QE dos.x output `<prefix>_dos.dat` for each system (EF in header,
same format plot_dos.py reads). Energies are shifted to E - EF so the two
systems can be overlaid; optional per-f.u. normalization columns included
(comp1 4 f.u. / modelc 5 f.u.) for fair visual comparison.

Usage:
    python3 export_dos_origin.py \
        --comp1 /path/comp1/V0_dos.dat --modelc /path/modelc/V0_dos.dat \
        --out docs/figures/slide05_dos_pdos/dos_overlay_origin.csv

Origin import: File > Import > CSV, first row = Long Name, second = Units.
Plot col B vs A (comp1) and D vs C (modelc) as Line; vertical line at x=0 = EF.
"""
import argparse
import re
from pathlib import Path

import numpy as np


def read_total_dos(dos_dat: Path):
    EF = None
    with open(dos_dat) as f:
        m = re.search(r"EFermi\s*=\s*([\-\d.]+)\s*eV", f.readline())
        if m:
            EF = float(m.group(1))
    data = np.loadtxt(dos_dat, comments="#")
    if EF is None:
        raise SystemExit(f"{dos_dat}: EFermi not found in header — dos.x output 맞는지 확인")
    return data[:, 0] - EF, data[:, 1], EF


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--comp1", required=True, help="comp1 <prefix>_dos.dat")
    ap.add_argument("--modelc", required=True, help="modelc <prefix>_dos.dat")
    ap.add_argument("--fu", type=float, nargs=2, default=[4.0, 5.0],
                    help="formula units per cell (comp1 modelc)")
    ap.add_argument("--out", default="dos_overlay_origin.csv")
    ap.add_argument("--png", default=None, help="optional preview PNG path")
    args = ap.parse_args()

    e1, d1, ef1 = read_total_dos(Path(args.comp1))
    e2, d2, ef2 = read_total_dos(Path(args.modelc))
    fu1, fu2 = args.fu

    n = max(len(e1), len(e2))
    pad = lambda a, n: np.pad(a, (0, n - len(a)), constant_values=np.nan)
    cols = [pad(e1, n), pad(d1, n), pad(d1 / fu1, n),
            pad(e2, n), pad(d2, n), pad(d2 / fu2, n)]

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    header = (
        "E-EF comp1,DOS comp1,DOS comp1 per f.u.,"
        "E-EF modelc,DOS modelc,DOS modelc per f.u.\n"
        "eV,states/eV/cell,states/eV/f.u.,eV,states/eV/cell,states/eV/f.u.\n"
        f"# EF(comp1)={ef1:.3f} eV  EF(modelc)={ef2:.3f} eV  f.u.={fu1:g}/{fu2:g}\n"
    )
    with open(out, "w") as f:
        f.write(header)
        np.savetxt(f, np.column_stack(cols), delimiter=",", fmt="%.6g")
    print(f"→ {out}  (EF comp1 {ef1:.3f} / modelc {ef2:.3f} eV)")

    if args.png:
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.plot(e1, d1 / fu1, color="#1f5fbf", lw=1.2, label="LPSCl (comp1)")
        ax.plot(e2, d2 / fu2, color="#c8102e", lw=1.2, label="LPSCl$_{1.6}$ (modelc)")
        ax.axvline(0, color="gray", ls="--", lw=0.9, label="$E_F$")
        ax.set_xlim(-8, 8)
        ax.set_ylim(bottom=0)
        ax.set_xlabel("E $-$ E$_F$ (eV)")
        ax.set_ylabel("DOS (states/eV/f.u.)")
        ax.legend(loc="upper left")
        ax.grid(alpha=0.3)
        plt.tight_layout()
        plt.savefig(args.png, dpi=200, facecolor="white", bbox_inches="tight")
        print(f"→ {args.png}")


if __name__ == "__main__":
    main()
