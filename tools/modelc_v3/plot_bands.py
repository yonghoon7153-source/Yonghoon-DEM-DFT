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


def reorder_bands_by_continuity(bands_mat, k_dist=None, segment_break_tol=0.05):
    """Re-assign band indices using a Hungarian-algorithm continuity matching.

    bands.x sorts eigenvalues by energy at each k-point. When two bands cross,
    the sorted index swaps and a band-index plot shows the "rogue" zig-zag
    that crosses the gap. Standard fix: at each k → k+1 transition, find the
    permutation of bands that minimises Σ|E_new[i] − E_prev[i]|, solved by
    scipy's linear_sum_assignment. This reconnects physical bands across all
    crossings without needing any symmetry/character info.

    Optional: detect segment breaks (large k-jump) and reset ordering at the
    new segment so we don't try to track across discontinuous directions.

    Args:
        bands_mat : (nbnd, nk) energy matrix.
        k_dist    : (nk,) cumulative k-distance (used to detect segment breaks).
        segment_break_tol : if successive k_dist differ by more than this, treat
                              as a new BZ segment (re-sort by energy from scratch).
    """
    from scipy.optimize import linear_sum_assignment
    nbnd, nk = bands_mat.shape
    out = bands_mat.copy()
    if k_dist is not None:
        dk = np.diff(k_dist)
        # typical step
        med_dk = float(np.median(dk[dk > 0])) if np.any(dk > 0) else 0.0
        seg_breaks = set(np.where(dk > max(segment_break_tol, 5 * med_dk))[0] + 1)
    else:
        seg_breaks = set()
    for ik in range(1, nk):
        if ik in seg_breaks:
            # don't try to match across a discontinuity — keep energy-sorted
            continue
        E_prev = out[:, ik - 1]
        E_curr = bands_mat[:, ik]
        cost = np.abs(E_prev[:, None] - E_curr[None, :])
        # solve linear assignment: row i (prev band index) ↔ col col_ind[i]
        row_ind, col_ind = linear_sum_assignment(cost)
        # row_ind is 0..nbnd-1 sorted; col_ind gives the matched current column
        out[:, ik] = bands_mat[col_ind, ik]
    return out


def parse_bands_gnu(dat_gnu_path):
    """Returns (k_dists, bands_matrix) — bands_matrix shape (nbnd, nk).

    QE bands.dat.gnu format: each band is a sequence of (k_dist, energy) lines.
    Bands are separated by blank lines OR are concatenated with no separator
    (depending on QE version). We robustly detect band boundaries by spotting
    where k_dist either resets to (≈)0 or decreases.
    """
    raw_lines = []
    for line in dat_gnu_path.read_text().splitlines():
        ln = line.strip()
        if not ln:
            raw_lines.append(None)  # blank-line marker
            continue
        parts = ln.split()
        if len(parts) >= 2:
            try:
                raw_lines.append((float(parts[0]), float(parts[1])))
            except ValueError:
                continue

    # Split into bands. Strategy:
    # 1) if blank-line markers present, split there
    # 2) else: detect k_dist reset (next k <= previous k by more than tolerance)
    bands_raw = []
    cur = []
    has_blanks = any(x is None for x in raw_lines)
    if has_blanks:
        for x in raw_lines:
            if x is None:
                if cur:
                    bands_raw.append(cur); cur = []
            else:
                cur.append(x)
        if cur:
            bands_raw.append(cur)
    else:
        prev_k = -1e9
        for x in raw_lines:
            k, e = x
            if k < prev_k - 1e-6 and cur:
                # k went backwards → new band
                bands_raw.append(cur); cur = []
            cur.append((k, e))
            prev_k = k
        if cur:
            bands_raw.append(cur)

    if not bands_raw:
        raise SystemExit(f"no bands parsed from {dat_gnu_path}")

    # Align all bands to same k-points (use first band's k as reference)
    k0 = np.array([p[0] for p in bands_raw[0]])
    mat = np.array([[p[1] for p in b] for b in bands_raw if len(b) == len(k0)])
    print(f"  parsed {mat.shape[0]} bands × {mat.shape[1]} k-points "
          f"(found {len(bands_raw)} band-blocks, kept those matching ref k-length)")
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

    # Hungarian-algorithm band continuity reassignment — removes the
    # "rogue diagonal" artifact that comes from energy-sorted indexing
    # across band crossings.
    bands_mat = reorder_bands_by_continuity(bands_mat, ks)
    print(f"  bands reordered by continuity (Hungarian)")

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
