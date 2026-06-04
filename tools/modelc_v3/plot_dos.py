#!/usr/bin/env python3
"""Total-DOS + element-resolved PDOS plot from QE dos.x / projwfc.x output.

Reads:
  - V0_dos.dat              (total DOS, EF in header)
  - V0_pdos.pdos_atm#N(El)_wfc#M(L)   (per-atom per-orbital PDOS)

Generates:
  - V0_dos_raw.png       — total DOS only, with EF and gap shading
  - V0_dos_pdos.png      — total + element-stacked PDOS (Li/P/S/Cl)
  - V0_dos_summary.json  — EF, VBM, CBM, gap, peak positions

VBM/CBM detection: scan E > -3 eV (skip semicores), find the longest
contiguous interval where DOS < threshold → that interval is the gap.

Usage:
    python3 plot_dos.py --dir /path/to/v3_post  \\
        --prefix V0 --out_prefix V0
"""
import argparse
import json
import re
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt


ELEM_COLOR = {
    "Li": "#888888",   # gray
    "P":  "#FF9933",   # orange
    "S":  "#E0C200",   # yellow-gold
    "Cl": "#3E8E41",   # green
}
ELEM_ORDER = ["Li", "P", "S", "Cl"]


def read_total_dos(dos_dat: Path):
    """Read V0_dos.dat. Returns (E, DOS, EF)."""
    EF = None
    with open(dos_dat) as f:
        head = f.readline()
        m = re.search(r"EFermi\s*=\s*([\-\d.]+)\s*eV", head)
        if m:
            EF = float(m.group(1))
    data = np.loadtxt(dos_dat, comments="#")
    E = data[:, 0]
    DOS = data[:, 1]
    return E, DOS, EF


def read_pdos_files(pdos_dir: Path, prefix: str):
    """Read all V0_pdos.pdos_atm#N(El)_wfc#M(L) files.

    Returns dict: element -> {"E": array, "PDOS": array}
    Sum over all atoms and orbitals per element.
    """
    pat = re.compile(rf"{re.escape(prefix)}_pdos\.pdos_atm#(\d+)\(([A-Za-z]+)\)_wfc#(\d+)\(([a-z])\)$")
    per_elem = {}  # element -> running sum of ldos
    E_ref = None
    for fp in sorted(pdos_dir.iterdir()):
        m = pat.match(fp.name)
        if not m:
            continue
        atom_idx, elem, wfc_idx, orb = m.groups()
        data = np.loadtxt(fp, comments="#")
        E = data[:, 0]
        # Col 1 is ldos (sum of m for that wfc); cols 2.. are m-resolved
        ldos = data[:, 1]
        if E_ref is None:
            E_ref = E
        if elem not in per_elem:
            per_elem[elem] = np.zeros_like(ldos)
        per_elem[elem] += ldos
    return E_ref, per_elem


def find_gap(E, DOS, EF, e_min=-3.0, dos_thresh=1e-3):
    """Find VBM/CBM by longest low-DOS interval above e_min.

    Returns (VBM, CBM, gap, VBM_peak, CBM_peak).
    """
    mask = E >= e_min
    Em = E[mask]; Dm = DOS[mask]
    low = Dm < dos_thresh
    # find contiguous runs of low
    best_start, best_len = -1, 0
    i = 0
    while i < len(low):
        if low[i]:
            j = i
            while j < len(low) and low[j]:
                j += 1
            if (j - i) > best_len:
                best_len = j - i
                best_start = i
            i = j
        else:
            i += 1
    if best_start < 0 or best_len < 3:
        return None, None, None, None, None
    vbm = float(Em[best_start - 1]) if best_start > 0 else float(Em[best_start])
    cbm = float(Em[best_start + best_len])
    gap = cbm - vbm
    # Peak positions = E with highest DOS on either side of the gap
    valence_mask = (E < vbm) & (E >= e_min)
    cond_mask = E > cbm
    vbm_peak = float(E[valence_mask][np.argmax(DOS[valence_mask])]) if valence_mask.any() else None
    cbm_peak = float(E[cond_mask][np.argmax(DOS[cond_mask])]) if cond_mask.any() else None
    return vbm, cbm, gap, vbm_peak, cbm_peak


def plot_raw(E, DOS, EF, vbm, cbm, out_path, xlim=(-15, 10)):
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(E, DOS, color="black", lw=1.0)
    ax.fill_between(E, 0, DOS, color="lightgray", alpha=0.6)
    if EF is not None:
        ax.axvline(EF, color="red", ls="--", lw=1.0, label=f"E$_F$ = {EF:.3f} eV")
    if vbm is not None and cbm is not None:
        ax.axvspan(vbm, cbm, color="lightyellow", alpha=0.5,
                   label=f"gap = {cbm - vbm:.3f} eV")
    ax.set_xlim(*xlim)
    ax.set_ylim(bottom=0)
    ax.set_xlabel("E − E$_{vac}$ (eV)")
    ax.set_ylabel("DOS (states/eV/cell)")
    ax.set_title("Total DOS")
    ax.legend(loc="upper left", fontsize=9)
    ax.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(out_path, dpi=200, facecolor="white", bbox_inches="tight")
    print(f"  → {out_path}")
    plt.close()


def plot_pdos(E, DOS, EF, vbm, cbm, E_p, per_elem, out_path, xlim=(-15, 10)):
    fig, ax = plt.subplots(figsize=(9, 5.5))
    # Total
    ax.plot(E, DOS, color="black", lw=1.2, label="Total")
    # Per element
    for el in ELEM_ORDER:
        if el in per_elem:
            ax.plot(E_p, per_elem[el], color=ELEM_COLOR[el], lw=1.2, label=el)
            ax.fill_between(E_p, 0, per_elem[el], color=ELEM_COLOR[el], alpha=0.3)
    if EF is not None:
        ax.axvline(EF, color="red", ls="--", lw=1.0, label=f"E$_F$ = {EF:.2f} eV")
    if vbm is not None and cbm is not None:
        ax.axvspan(vbm, cbm, color="lightyellow", alpha=0.4,
                   label=f"gap = {cbm - vbm:.2f} eV")
    ax.set_xlim(*xlim)
    ax.set_ylim(bottom=0)
    ax.set_xlabel("E (eV)")
    ax.set_ylabel("DOS / PDOS (states/eV/cell)")
    ax.set_title("Total DOS + element-resolved PDOS")
    ax.legend(loc="upper left", fontsize=9, ncol=2)
    ax.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(out_path, dpi=200, facecolor="white", bbox_inches="tight")
    print(f"  → {out_path}")
    plt.close()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", required=True, help="dir with V0_dos.dat and V0_pdos.* files")
    ap.add_argument("--prefix", default="V0", help="output filename prefix (default V0)")
    ap.add_argument("--out_prefix", default=None, help="prefix for png/json (default = --prefix)")
    ap.add_argument("--e_min", type=float, default=-3.0,
                    help="lower E cutoff for gap search (skip semicores)")
    ap.add_argument("--dos_thresh", type=float, default=1e-3,
                    help="DOS threshold to be considered 'in the gap'")
    ap.add_argument("--xlim", type=float, nargs=2, default=[-15, 10])
    args = ap.parse_args()

    d = Path(args.dir)
    out_pref = args.out_prefix or args.prefix
    dos_dat = d / f"{args.prefix}_dos.dat"
    E, DOS, EF = read_total_dos(dos_dat)
    print(f"read total DOS: {len(E)} points, EF = {EF}")

    E_p, per_elem = read_pdos_files(d, args.prefix)
    for el, p in per_elem.items():
        print(f"  PDOS sum for {el}: integral = {np.trapezoid(p, E_p):.3f} states")

    vbm, cbm, gap, vbm_peak, cbm_peak = find_gap(
        E, DOS, EF, e_min=args.e_min, dos_thresh=args.dos_thresh)
    print(f"VBM={vbm} CBM={cbm} gap={gap}")

    summary = {
        "EF_eV_qe": EF,
        "VBM_eV": vbm,
        "CBM_eV": cbm,
        "band_gap_eV": gap,
        "VBM_peak_eV": vbm_peak,
        "CBM_peak_eV": cbm_peak,
        "method": f"longest low-DOS run (DOS<{args.dos_thresh}) restricted to E > {args.e_min} eV (above semicores)",
    }
    json_path = d / f"{out_pref}_dos_summary.json"
    json_path.write_text(json.dumps(summary, indent=2))
    print(f"  → {json_path}")

    plot_raw(E, DOS, EF, vbm, cbm, d / f"{out_pref}_dos_raw.png", xlim=tuple(args.xlim))
    plot_pdos(E, DOS, EF, vbm, cbm, E_p, per_elem,
              d / f"{out_pref}_dos_pdos.png", xlim=tuple(args.xlim))


if __name__ == "__main__":
    main()
