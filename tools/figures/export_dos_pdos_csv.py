#!/usr/bin/env python3
"""export_dos_pdos_csv.py — clean, figure-matching DOS/PDOS CSV.
Reads a *_pdos_compact.csv (E-EF, total, <elements>), trims to the valence
window (drops Li-1s semicore etc.), Gaussian-broadens each column, reorders
columns, and writes a tidy CSV for Origin re-plot. Matches the 0.15 eV figures.

Usage:
  python3 export_dos_pdos_csv.py --csv docs/figures/modelc_pdos_compact.csv \
     --out docs/figures/dos_pdos_smooth/modelc_dos_pdos_0.15.csv \
     --order S P Cl Li --gap 2.10 --label "modelC (LPSCl1.6)"
"""
import argparse, csv
import numpy as np
try:
    from scipy.ndimage import gaussian_filter1d
    def smooth(y, s_pts): return gaussian_filter1d(y, s_pts)
except Exception:
    def smooth(y, s_pts):
        n = max(1, int(round(4 * s_pts))); x = np.arange(-n, n + 1)
        k = np.exp(-0.5 * (x / s_pts) ** 2); k /= k.sum()
        return np.convolve(y, k, mode="same")

ap = argparse.ArgumentParser()
ap.add_argument("--csv", required=True)
ap.add_argument("--out", required=True)
ap.add_argument("--order", nargs="+", required=True, help="element column order")
ap.add_argument("--window", type=float, nargs=2, default=[-8.0, 5.0])
ap.add_argument("--sigma", type=float, default=0.15)
ap.add_argument("--gap", type=float, default=None)
ap.add_argument("--label", default="")
a = ap.parse_args()

rows = list(csv.reader(open(a.csv)))
hdr = [h.split("#")[0].strip() for h in rows[0]]          # strip trailing "# ..."
data = np.array([[float(x) for x in r[:len(hdr)]] for r in rows[1:] if r])
col = {h: data[:, i] for i, h in enumerate(hdr)}
E = col["E-EF"]
m = (E >= a.window[0]) & (E <= a.window[1])
E = E[m]
dE = np.median(np.diff(E))
s_pts = a.sigma / dE

out_cols = ["total"] + list(a.order)
# Nd: also sum 4f sub-columns if present
extra = {}
if "Nd" in col and "Nd1_4f" in col and "Nd2_4f" in col:
    extra["Nd_4f"] = col["Nd1_4f"][m] + col["Nd2_4f"][m]

with open(a.out, "w", newline="") as f:
    w = csv.writer(f)
    tag = f" gap={a.gap} eV," if a.gap else ""
    w.writerow([f"# {a.label} DOS/PDOS (states/eV),{tag} Gaussian sigma={a.sigma} eV, EF=0, bonding=below 0"])
    head = ["E_minus_EF_eV"] + [f"DOS_{c}" for c in out_cols] + [f"DOS_{k}" for k in extra]
    w.writerow(head)
    sm = {c: smooth(col[c][m], s_pts) for c in out_cols}
    sm.update({k: smooth(v, s_pts) for k, v in extra.items()})
    for i, e in enumerate(E):
        w.writerow([f"{e:.3f}"] + [f"{sm[c][i]:.4f}" for c in out_cols]
                   + [f"{sm[k][i]:.4f}" for k in extra])
print(f"-> {a.out}  ({m.sum()} rows, {a.window[0]}..{a.window[1]} eV, sigma {a.sigma})")
