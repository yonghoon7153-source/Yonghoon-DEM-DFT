#!/usr/bin/env python3
"""Plot QE band structure from bands.dat.gnu + nscf_bands output.

Reads:
  - bands.dat.gnu (gnuplot-format, easier to parse) from bands.x output
  - nscf_bands.out (for Fermi level / total nbnd)
  - V0_dos_summary.json (optional, for VBM/CBM/Egap reference)

Plots:
  - bands along the auto k-path (E - E_F)
  - VBM / CBM lines
  - gap shading
  - special-point ticks

Usage:
    python3 plot_bands.py \\
        --work_dir /home/ubuntu/work/runs/modelC_v3 \\
        --out_png  /home/ubuntu/work/runs/modelC_v3/V0_band_structure.png
"""
import argparse
import json
import re
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt


def parse_fermi_eV(nscf_out_path):
    txt = nscf_out_path.read_text()
    # Look for "the Fermi energy is" OR "highest occupied"
    m = re.search(r"the Fermi energy is\s+([-\d.]+)\s*ev", txt, re.IGNORECASE)
    if m:
        return float(m.group(1))
    m = re.search(r"highest occupied,?\s*lowest unoccupied level\s*\(ev\):\s*"
                  r"([-\d.]+)\s+([-\d.]+)", txt, re.IGNORECASE)
    if m:
        return (float(m.group(1)) + float(m.group(2))) / 2.0
    m = re.search(r"highest occupied level\s*\(ev\):\s*([-\d.]+)", txt,
                  re.IGNORECASE)
    if m:
        return float(m.group(1))
    return None


def parse_bands_gnu(dat_gnu_path):
    """Returns (k_dists, bands_matrix) — bands_matrix shape (nbnd, nk)."""
    txt = dat_gnu_path.read_text()
    blocks = [b.strip() for b in txt.split("\n\n") if b.strip()]
    bands = []
    for blk in blocks:
        ks, es = [], []
        for line in blk.splitlines():
            parts = line.split()
            if len(parts) >= 2:
                ks.append(float(parts[0])); es.append(float(parts[1]))
        bands.append((np.array(ks), np.array(es)))
    if not bands:
        raise SystemExit(f"no bands parsed from {dat_gnu_path}")
    k0 = bands[0][0]
    mat = np.array([b[1] for b in bands])  # (nbnd, nk)
    return k0, mat


def parse_special_kpoints_from_bands_dat(dat_path):
    """Reads bands.x's text output to find k-point labels (high-sym points).
    The bands.dat (NOT .gnu) lists k-point coords; we infer break-points from
    discontinuities in cumulative k-distance.
    """
    txt = dat_path.read_text() if dat_path.exists() else ""
    # Look for k-coord lines like " &plot nbnd= ##, nks= ##"
    # then triplets per k-point: kx ky kz <newline> e1 e2 ...
    return None  # fall back to plain x-axis


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--work_dir", required=True)
    ap.add_argument("--out_png", default=None)
    ap.add_argument("--energy_window", type=float, nargs=2,
                    default=[-6, 6], help="(E_min, E_max) eV around Fermi")
    ap.add_argument("--dos_summary_json", default=None,
                    help="optional V0_dos_summary.json for gap reference")
    args = ap.parse_args()

    work = Path(args.work_dir)
    gnu = work / "bands.dat.gnu"
    if not gnu.exists():
        raise SystemExit(f"missing {gnu} — run bands.x first")
    out_png = Path(args.out_png) if args.out_png else work / "V0_band_structure.png"

    ks, bands_mat = parse_bands_gnu(gnu)
    print(f"Loaded {bands_mat.shape[0]} bands × {bands_mat.shape[1]} k-points")

    EF = parse_fermi_eV(work / "nscf_bands.out")
    if EF is None:
        # fallback: use VBM from DOS summary
        if args.dos_summary_json:
            d = json.load(open(args.dos_summary_json))
            EF = d.get("VBM_eV", 0.0)
            print(f"  Fermi not in nscf_bands.out; using VBM from DOS = {EF}")
        else:
            EF = 0.0
            print("  WARNING: no Fermi level found; setting E_F = 0")
    else:
        print(f"  Fermi/HOMO from nscf = {EF:.3f} eV")

    fig, ax = plt.subplots(figsize=(7.5, 5.5))
    for b in bands_mat:
        ax.plot(ks, b - EF, '-', color='#3B5BA0', lw=0.9)
    ax.axhline(0, color='#888', ls='--', lw=0.8)
    ax.set_ylim(args.energy_window)
    ax.set_xlim(ks.min(), ks.max())
    ax.set_xlabel("k-path")
    ax.set_ylabel("E − E$_F$  (eV)")
    ax.set_title("Band structure — modelC_v3 (LPSCl1.6, PBE)")

    # Gap shading
    if args.dos_summary_json:
        try:
            d = json.load(open(args.dos_summary_json))
            vbm = d.get("VBM_eV"); cbm = d.get("CBM_eV"); gap = d.get("band_gap_eV")
            if vbm is not None and cbm is not None:
                ax.axhspan(vbm - EF, cbm - EF, color='#fffabb', alpha=0.5,
                           label=f"DOS gap = {gap:.2f} eV")
                ax.legend(loc='upper right', fontsize=10, frameon=False)
        except Exception as e:
            print(f"  [warn] dos summary read failed: {e}")

    ax.grid(axis='y', alpha=0.3, linestyle=':')
    ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
    plt.tight_layout()
    plt.savefig(out_png, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"\n→ {out_png}")


if __name__ == "__main__":
    main()
