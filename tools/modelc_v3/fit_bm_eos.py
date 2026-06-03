#!/usr/bin/env python3
"""Fit 3rd-order Birch-Murnaghan EOS to E(V) from a modelC_v3 BM-EOS sweep.

Reads v00.out ... vNN.out from <dir>, extracts (V, E) pairs, fits BM3.
Outputs JSON + PNG plot.

Usage:
    python3 fit_bm_eos.py --dir /home/.../bm_eos --out bm_eos_results.json
"""
import argparse
import json
import re
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


RY_TO_EV = 13.605693122994
BOHR_TO_A = 0.5291772108


def bm3(V, V0, E0, B0_GPa, B0p):
    """Birch–Murnaghan 3rd-order. B0 in GPa, V in Å³, E in eV.
    Converts B0_GPa to eV/Å³ for the formula: 1 GPa = 1/160.21766208 eV/Å³.
    """
    B0 = B0_GPa / 160.21766208  # eV / Å³
    eta = (V0 / V) ** (2.0 / 3.0)
    return E0 + (9.0 * V0 * B0 / 16.0) * (
        (eta - 1.0) ** 3 * B0p +
        (eta - 1.0) ** 2 * (6.0 - 4.0 * eta)
    )


def parse_volume_and_energy(out_path):
    """Return (V_A3, E_eV) from a relax output (last !! line)."""
    text = out_path.read_text()
    # Last "!    total energy" line gives final converged E
    m_e = re.findall(r"!\s+total energy\s+=\s+(-?\d+\.\d+)\s+Ry", text)
    if not m_e:
        return None, None
    E_eV = float(m_e[-1]) * RY_TO_EV

    # Volume in Bohr^3 from "unit-cell volume" line (BFGS prints initial only;
    # for fixed-cell relax, V doesn't change, so first one is fine).
    m_v = re.search(r"unit-cell volume\s+=\s+([\d.]+)\s+\(a\.u\.\)\^3", text)
    if not m_v:
        return None, E_eV
    V_A3 = float(m_v.group(1)) * BOHR_TO_A ** 3
    return V_A3, E_eV


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", required=True)
    ap.add_argument("--pattern", default="v*.out")
    ap.add_argument("--out", default=None)
    ap.add_argument("--out_png", default=None)
    args = ap.parse_args()

    d = Path(args.dir)
    files = sorted(d.glob(args.pattern))
    if not files:
        raise SystemExit(f"no files matched {args.pattern} in {d}")

    Vs, Es, names = [], [], []
    for f in files:
        V, E = parse_volume_and_energy(f)
        if V is None or E is None:
            print(f"  [skip] {f.name}: missing V or E")
            continue
        Vs.append(V); Es.append(E); names.append(f.name)
        print(f"  {f.name}: V = {V:.4f} Å³, E = {E:.6f} eV")

    if len(Vs) < 4:
        raise SystemExit(f"need ≥4 points for BM3 fit, got {len(Vs)}")

    Vs = np.array(Vs); Es = np.array(Es)

    # Initial guesses
    V0_guess = Vs[np.argmin(Es)]
    E0_guess = Es.min()
    p0 = [V0_guess, E0_guess, 20.0, 4.0]  # B0=20 GPa, B0'=4

    try:
        popt, pcov = curve_fit(bm3, Vs, Es, p0=p0, maxfev=20000)
    except RuntimeError as e:
        raise SystemExit(f"BM3 fit failed: {e}")
    V0, E0, B0_GPa, B0p = popt
    perr = np.sqrt(np.diag(pcov))

    # R²
    E_fit = bm3(Vs, *popt)
    ss_res = ((Es - E_fit) ** 2).sum()
    ss_tot = ((Es - Es.mean()) ** 2).sum()
    R2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else 0.0

    print(f"\n=== BM3 fit ===")
    print(f"  V0  = {V0:.4f} ± {perr[0]:.4f} Å³")
    print(f"  E0  = {E0:.6f} ± {perr[1]:.6f} eV")
    print(f"  B0  = {B0_GPa:.3f} ± {perr[2]:.3f} GPa")
    print(f"  B0' = {B0p:.3f} ± {perr[3]:.3f}")
    print(f"  R²  = {R2:.6f}")
    print(f"  n_points = {len(Vs)}")

    # Plot
    out_png = Path(args.out_png) if args.out_png else d / "bm_eos_fit.png"
    fig, ax = plt.subplots(figsize=(7, 5))
    V_dense = np.linspace(Vs.min() * 0.99, Vs.max() * 1.01, 200)
    E_dense = bm3(V_dense, *popt)
    ax.plot(V_dense, E_dense, '-', color='#3B5BA0', lw=2,
            label=f"BM3: B₀ = {B0_GPa:.2f} GPa, B₀′ = {B0p:.2f}")
    ax.plot(Vs, Es, 'o', mfc='#C44536', mec='k', mew=0.8, ms=10,
            label=f"DFT points ({len(Vs)})")
    ax.axvline(V0, color='#666', ls='--', lw=0.8,
                label=f"V₀ = {V0:.2f} Å³")
    ax.set_xlabel("Volume (Å³)", fontsize=12)
    ax.set_ylabel("Total energy (eV)", fontsize=12)
    ax.set_title(f"BM3 EOS — modelC_v3 (LPSCl1.6),  R² = {R2:.5f}",
                  fontsize=12)
    ax.legend(loc='best', fontsize=10, frameon=False)
    ax.grid(alpha=0.3, ls='--')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.tight_layout()
    plt.savefig(out_png, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"\n→ {out_png}")

    # JSON
    out_json = Path(args.out) if args.out else d / "bm_eos_results.json"
    summary = {
        "method": "3rd-order Birch-Murnaghan",
        "system": "modelC_v3 (Li5.4PS4.4Cl1.6)",
        "n_points": len(Vs),
        "fit": {
            "V0_A3": float(V0),
            "V0_std": float(perr[0]),
            "E0_eV": float(E0),
            "E0_std": float(perr[1]),
            "B0_GPa": float(B0_GPa),
            "B0_std_GPa": float(perr[2]),
            "B0_prime": float(B0p),
            "B0_prime_std": float(perr[3]),
            "R_squared": float(R2),
        },
        "data_points": [
            {"file": names[i], "V_A3": float(Vs[i]), "E_eV": float(Es[i])}
            for i in range(len(Vs))
        ],
    }
    out_json.write_text(json.dumps(summary, indent=2))
    print(f"→ {out_json}")


if __name__ == "__main__":
    main()
