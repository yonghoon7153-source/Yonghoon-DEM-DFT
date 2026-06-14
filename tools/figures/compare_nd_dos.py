#!/usr/bin/env python3
"""Matched-k defect-band comparison: undoped modelc vs Nd2O3-doped (paper #2 electronic).

The electronic-conduction story is NOT band-gap width — it is the DEFECT BAND / states
at E_F. Undoped modelc (disorder: Li vac + 4d-Cl anti-sites) has S 3p hole states that
push E_F below the valence top -> finite DOS(E_F) = electronic-leakage channel
(paper #1: 0.74 unoccupied valence-top states). Nd2O3 doping: O2- passivates those holes
-> E_F back in a clean gap, DOS(E_F)=0.

This reads BOTH dos.x outputs (each with its own EFermi in the header), aligns to E-E_F,
and reports the matched discriminators:
  - DOS(E_F)                         (>0 = electronic states at Fermi level = leakage)
  - integrated states in [E_F+-0.5]  (defect-band weight near E_F)
  - VBM, CBM relative to E_F; whether E_F sits below the valence top (holes)
Both are normalized per formula unit (P count = f.u.) for a fair cell-size comparison.
Also writes a compact overlay CSV (E-E_F, doped, undoped) over [-3,3] eV for the figure.

Usage (KISTI, uma env):
  python3 compare_nd_dos.py \
    --undoped undoped_ref_k661/U0_dos.dat --undoped_fu 10 \
    --doped   .../v0_champion/V0_dos.dat  --doped_fu 10 \
    --out_csv nd_defectband_overlay.csv
Paste the printed table + the CSV; figure is built from the CSV.
"""
import argparse
import re
import numpy as np


def load(path):
    """Return (E, total_DOS) ; total = col1 (nspin1) or col1+col2 (nspin2); EF from header."""
    hdr = open(path).readline()
    EF = float(re.search(r"EFermi\s*=\s*([\-\d.]+)", hdr).group(1))
    d = np.loadtxt(path)
    # nspin=2 dos.x: E, dosup, dosdw, intdos ; nspin=1: E, dos, intdos
    tot = d[:, 1] + d[:, 2] if "dosdw" in hdr or "dosup" in hdr else d[:, 1]
    return d[:, 0] - EF, tot, EF


def metrics(E, tot, fu, label):
    dosEF = float(np.interp(0.0, E, tot)) / fu
    win = (E > -0.5) & (E < 0.5)
    near_EF = float(np.trapezoid(tot[win], E[win])) / fu if win.any() else 0.0
    # valence top: highest E<0 region with DOS>0.5/cell; CBM: lowest E>0 with DOS>0.5/cell
    thr = 0.5
    occ = E[(tot > thr) & (E < 0)]
    vir = E[(tot > thr) & (E > 0)]
    vbm = occ.max() if occ.size else float("nan")
    cbm = vir.min() if vir.size else float("nan")
    print(f"  [{label}]  DOS(E_F)/fu = {dosEF:.4f}   states[E_F+-0.5]/fu = {near_EF:.4f}")
    print(f"            valence top (rel E_F) = {vbm:+.2f}   conduction edge = {cbm:+.2f}"
          f"   {'E_F INSIDE valence (HOLES -> leakage)' if vbm>0.02 else 'E_F in gap (clean)'}")
    return dosEF, near_EF, vbm, cbm


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--undoped", required=True)
    ap.add_argument("--doped", required=True)
    ap.add_argument("--undoped_fu", type=float, default=10.0)
    ap.add_argument("--doped_fu", type=float, default=10.0)
    ap.add_argument("--out_csv", default="nd_defectband_overlay.csv")
    A = ap.parse_args()

    Eu, Tu, EFu = load(A.undoped)
    Ed, Td, EFd = load(A.doped)
    print(f"EFermi: undoped={EFu:.3f}  doped={EFd:.3f} eV   (axes shifted to E-E_F)")
    print("=== matched defect-band metrics (per f.u.) ===")
    mu = metrics(Eu, Tu, A.undoped_fu, "undoped modelc")
    md = metrics(Ed, Td, A.doped_fu, "Nd2O3-doped")
    print("\n=== verdict ===")
    print(f"  DOS(E_F): undoped {mu[0]:.4f} -> doped {md[0]:.4f} /fu"
          f"   (clean if doped ~0; undoped >0 = defect band)")
    if mu[0] > 1e-3:
        print(f"  near-E_F states: undoped {mu[1]:.3f} -> doped {md[1]:.3f}"
              f"  => {mu[1]/max(md[1],1e-4):.0f}x reduction (electronic-conduction channel suppressed)")

    # compact overlay CSV for the figure (per f.u.), zoomed window
    grid = np.arange(-3.0, 3.001, 0.02)
    du = np.interp(grid, Eu, Tu) / A.undoped_fu
    dd = np.interp(grid, Ed, Td) / A.doped_fu
    with open(A.out_csv, "w") as f:
        f.write("E-EF,undoped,doped\n")
        for i in range(len(grid)):
            f.write(f"{grid[i]:.3f},{du[i]:.5g},{dd[i]:.5g}\n")
    print(f"\n-> {A.out_csv}  ({len(grid)} rows, E-E_F in [-3,3], per f.u.) — paste this for the figure")


if __name__ == "__main__":
    main()
