#!/usr/bin/env python3
"""BM3 fit for DFT EOS scan + closest grid selection for V0 structure.

Reads N pw.out files from EOS scan, extracts (V, E), fits 3rd-order
Birch-Murnaghan, identifies grid point closest to V0_fit (used as V0
structure for post-processing: tight SCF, NSCF, PDOS, Bader, elastic).

Usage:
    python bm3_fit_eos.py \\
        --pattern 'comp2_v2_eos_v*.out' \\
        --label comp2_v2 \\
        --out comp2_v2_BM3_fit.json

Output JSON:
    V0_A3, E0_eV, B0_GPa, B0_prime, closest_grid{vol_label, V, delta_pct}, raw_data
"""
import argparse
import glob
import json
import re
from pathlib import Path

import numpy as np
from ase.io import read
from scipy.optimize import curve_fit


def BM(V, E0, V0, B0, B0p):
    """Birch-Murnaghan 3rd order EOS (energy form)."""
    eta = (V0 / V) ** (2 / 3)
    return E0 + 9 * V0 * B0 / 16 * ((eta - 1) ** 3 * B0p + (eta - 1) ** 2 * (6 - 4 * eta))


def parse_pwout(pwout):
    """Last frame V (Å³) and total E (eV) from QE relax output."""
    atoms = read(pwout, format='espresso-out', index=-1)
    return atoms.get_volume(), atoms.get_potential_energy()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--pattern', required=True,
                    help="glob pattern, e.g. 'comp2_v2_eos_v*.out'")
    ap.add_argument('--label', default='system')
    ap.add_argument('--out', default='BM3_fit.json')
    args = ap.parse_args()

    files = sorted(glob.glob(args.pattern))
    if len(files) < 5:
        raise SystemExit(f"need >=5 EOS files, found {len(files)}: {files}")

    raw = []
    for f in files:
        m = re.search(r'v(\d{3})', f)
        vlabel = f"v{m.group(1)}" if m else Path(f).stem
        V, E = parse_pwout(f)
        raw.append({"vol_label": vlabel, "V_A3": V, "E_eV": E, "file": f})
        print(f"  {vlabel}: V={V:.2f} A^3, E={E:.4f} eV")

    V_arr = np.array([r["V_A3"] for r in raw])
    E_arr = np.array([r["E_eV"] for r in raw])

    # initial guess: E0=Emin, V0=V@Emin, B0~20 GPa (eV/A^3), B0'=4
    p0 = [E_arr.min(), V_arr[np.argmin(E_arr)], 20.0 / 160.2, 4.0]
    popt, _ = curve_fit(BM, V_arr, E_arr, p0, maxfev=10000)
    E0, V0, B0, B0p = popt
    B0_GPa = B0 * 160.2

    R2 = 1 - np.sum((E_arr - BM(V_arr, *popt)) ** 2) / np.sum((E_arr - E_arr.mean()) ** 2)

    # closest grid for V0 structure
    idx_close = int(np.argmin(np.abs(V_arr - V0)))
    closest = raw[idx_close]
    delta_pct = 100 * (closest["V_A3"] - V0) / V0

    result = {
        "system": args.label,
        "n_points": len(raw),
        "V0_A3": float(V0),
        "E0_eV": float(E0),
        "B0_GPa": float(B0_GPa),
        "B0_prime": float(B0p),
        "R_squared": float(R2),
        "closest_grid": {
            "vol_label": closest["vol_label"],
            "V_A3": float(closest["V_A3"]),
            "delta_V_pct": float(delta_pct),
            "file": closest["file"],
        },
        "raw_data": raw,
    }

    Path(args.out).write_text(json.dumps(result, indent=2))

    print(f"\n=== BM3 fit ({args.label}) ===")
    print(f"  V0      = {V0:.4f} A^3")
    print(f"  B0      = {B0_GPa:.2f} GPa")
    print(f"  B0'     = {B0p:.4f}")
    print(f"  R^2     = {R2:.6f}")
    print(f"  closest = {closest['vol_label']} (Δ = {delta_pct:+.3f}%)")
    print(f"\n  → Use {closest['vol_label']}'s final cell + ATOMIC_POSITIONS as V0 structure")
    print(f"  Saved: {args.out}")


if __name__ == '__main__':
    main()
