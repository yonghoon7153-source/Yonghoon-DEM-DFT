#!/usr/bin/env python3
"""Paper-grade total-DOS + element-resolved PDOS from QE dos.x / projwfc.x output.

Reads:
  - <prefix>_dos.dat                          (total DOS, EF in header)
  - <prefix>_pdos.pdos_atm#N(El)_wfc#M(L)     (per-atom per-orbital PDOS)

Generates:
  - <out>_dos_raw.png        — total DOS only, with EF and gap shading
  - <out>_dos_pdos.png       — total + element-stacked PDOS (Li/P/S/Cl)
  - <out>_dos_summary.json   — EF, VBM, CBM, gap, peak positions, and
                               VBM/CBM orbital character

Algorithm notes:
  - Gap detection: contiguous interval of DOS < dos_thresh above e_min
    (skip deep semicores). Prefer the run straddling EF; otherwise longest.
  - VBM_peak / CBM_peak: closest local DOS maximum to VBM (below) / CBM (above)
    with min_height filter to ignore broadening noise.
  - VBM/CBM character: integrate each (element, orbital) PDOS over the
    0.5 eV window adjacent to the edge → percentages.

Usage:
    python3 plot_dos.py --dir /path/to/output --prefix V0 --out_prefix V0
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
    "Br": "#A0522D",   # sienna
    "O":  "#D62728",   # red
    "Nd": "#17BECF",   # teal
}
ELEM_ORDER = ["Li", "P", "S", "Cl", "Br", "O", "Nd"]
ORB_LABEL = {"s": "s", "p": "p", "d": "d", "f": "f"}


def read_total_dos(dos_dat: Path):
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
    """Returns (E, per_elem, per_elem_orb)
    per_elem[el]:        summed PDOS over all atoms & orbitals of element el
    per_elem_orb[el][o]: summed PDOS for orbital o ('s','p','d','f') of element el
    """
    pat = re.compile(rf"{re.escape(prefix)}_pdos\.pdos_atm#(\d+)\(([A-Za-z]+)\)_wfc#(\d+)\(([a-z])\)$")
    per_elem = {}
    per_elem_orb = {}
    E_ref = None
    for fp in sorted(pdos_dir.iterdir()):
        m = pat.match(fp.name)
        if not m:
            continue
        _, elem, _, orb = m.groups()
        data = np.loadtxt(fp, comments="#")
        E = data[:, 0]
        ldos = data[:, 1]
        if E_ref is None:
            E_ref = E
        per_elem.setdefault(elem, np.zeros_like(ldos))
        per_elem[elem] += ldos
        per_elem_orb.setdefault(elem, {})
        per_elem_orb[elem].setdefault(orb, np.zeros_like(ldos))
        per_elem_orb[elem][orb] += ldos
    return E_ref, per_elem, per_elem_orb


def find_gap(E, DOS, EF, e_min=-3.0, dos_thresh=0.5):
    mask = E >= e_min
    Em = E[mask]; Dm = DOS[mask]
    low = Dm < dos_thresh
    runs = []
    i = 0
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
        return None, None, None
    chosen = None
    if EF is not None:
        for (s, n) in runs:
            e_lo = Em[s]
            e_hi = Em[min(s + n - 1, len(Em) - 1)]
            if e_lo <= EF <= e_hi:
                chosen = (s, n)
                break
    if chosen is None:
        chosen = max(runs, key=lambda r: r[1])
    s, n = chosen
    vbm_idx = max(s - 1, 0)
    cbm_idx = min(s + n, len(Em) - 1)
    return float(Em[vbm_idx]), float(Em[cbm_idx]), float(Em[cbm_idx] - Em[vbm_idx])


def local_maxima(E, DOS, min_height=1.0):
    """Returns list of (E, DOS) at local maxima above min_height."""
    peaks = []
    for i in range(1, len(DOS) - 1):
        if DOS[i] > DOS[i - 1] and DOS[i] >= DOS[i + 1] and DOS[i] >= min_height:
            peaks.append((float(E[i]), float(DOS[i])))
    return peaks


def closest_peak_below(peaks, edge):
    cand = [p for p in peaks if p[0] < edge]
    return max(cand, key=lambda p: p[0]) if cand else None  # largest E < edge


def closest_peak_above(peaks, edge):
    cand = [p for p in peaks if p[0] > edge]
    return min(cand, key=lambda p: p[0]) if cand else None  # smallest E > edge


def character_at_edge(E_p, per_elem_orb, edge, window, side):
    """Integrate per-(elem, orb) PDOS over [edge - window, edge] for VBM (side='valence')
    or [edge, edge + window] for CBM (side='conduction'). Returns sorted percent breakdown.
    """
    if side == "valence":
        lo, hi = edge - window, edge
    else:
        lo, hi = edge, edge + window
    mask = (E_p >= lo) & (E_p <= hi)
    if not mask.any():
        return []
    contribs = []
    total = 0.0
    for el, orb_d in per_elem_orb.items():
        for orb, p in orb_d.items():
            I = float(np.trapezoid(p[mask], E_p[mask]))
            if I > 0:
                contribs.append((el, orb, I))
                total += I
    if total <= 0:
        return []
    contribs.sort(key=lambda x: -x[2])
    return [{"element": el, "orbital": orb, "percent": round(100 * I / total, 1)}
            for (el, orb, I) in contribs if (100 * I / total) >= 1.0]


def format_character(breakdown, top_n=3):
    if not breakdown:
        return None
    parts = [f"{b['element']} {b['orbital']} ({b['percent']:.0f}%)" for b in breakdown[:top_n]]
    return " + ".join(parts)


def plot_raw(E, DOS, EF, vbm, cbm, vbm_peak, cbm_peak, gap, out_path,
             xlim=(-15, 10), title="Total DOS"):
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(E, DOS, color="black", lw=1.0)
    ax.fill_between(E, 0, DOS, color="lightgray", alpha=0.6)
    if EF is not None:
        ax.axvline(EF, color="red", ls="--", lw=1.0, label=f"E$_F$ = {EF:.3f} eV")
    if vbm is not None and cbm is not None:
        ax.axvspan(vbm, cbm, color="lightyellow", alpha=0.6,
                   label=f"gap = {gap:.2f} eV ({vbm:.2f} → {cbm:.2f})")
    if vbm_peak is not None:
        ax.axvline(vbm_peak[0], color="#0066CC", ls=":", lw=0.9, alpha=0.7)
        ax.annotate(f"VBM peak\n{vbm_peak[0]:.2f}", xy=(vbm_peak[0], vbm_peak[1]),
                    xytext=(-30, 10), textcoords="offset points",
                    fontsize=8, color="#0066CC",
                    arrowprops=dict(arrowstyle="-", lw=0.7, color="#0066CC"))
    if cbm_peak is not None:
        ax.axvline(cbm_peak[0], color="#CC0066", ls=":", lw=0.9, alpha=0.7)
        ax.annotate(f"CBM peak\n{cbm_peak[0]:.2f}", xy=(cbm_peak[0], cbm_peak[1]),
                    xytext=(10, 10), textcoords="offset points",
                    fontsize=8, color="#CC0066",
                    arrowprops=dict(arrowstyle="-", lw=0.7, color="#CC0066"))
    ax.set_xlim(*xlim)
    ax.set_ylim(bottom=0)
    ax.set_xlabel("E (eV)")
    ax.set_ylabel("DOS (states/eV/cell)")
    ax.set_title(title)
    ax.legend(loc="upper left", fontsize=9)
    ax.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(out_path, dpi=200, facecolor="white", bbox_inches="tight")
    print(f"  → {out_path}")
    plt.close()


def plot_pdos(E, DOS, EF, vbm, cbm, gap, E_p, per_elem,
              vbm_char, cbm_char, out_path, xlim=(-15, 10), title=None):
    fig, ax = plt.subplots(figsize=(9, 5.5))
    ax.plot(E, DOS, color="black", lw=1.2, label="Total")
    for el in ELEM_ORDER:
        if el in per_elem:
            ax.plot(E_p, per_elem[el], color=ELEM_COLOR[el], lw=1.2, label=el)
            ax.fill_between(E_p, 0, per_elem[el], color=ELEM_COLOR[el], alpha=0.3)
    if EF is not None:
        ax.axvline(EF, color="red", ls="--", lw=1.0, label=f"E$_F$ = {EF:.2f} eV")
    if vbm is not None and cbm is not None:
        ax.axvspan(vbm, cbm, color="lightyellow", alpha=0.5,
                   label=f"gap = {gap:.2f} eV")
    ax.set_xlim(*xlim)
    ax.set_ylim(bottom=0)
    ax.set_xlabel("E (eV)")
    ax.set_ylabel("DOS / PDOS (states/eV/cell)")
    t = title or "Total DOS + element-resolved PDOS"
    if vbm_char and cbm_char:
        t += f"\nVBM: {vbm_char}    CBM: {cbm_char}"
    ax.set_title(t, fontsize=11)
    ax.legend(loc="upper left", fontsize=9, ncol=2)
    ax.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(out_path, dpi=200, facecolor="white", bbox_inches="tight")
    print(f"  → {out_path}")
    plt.close()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", required=True)
    ap.add_argument("--prefix", default="V0")
    ap.add_argument("--out_prefix", default=None)
    ap.add_argument("--e_min", type=float, default=-3.0)
    ap.add_argument("--dos_thresh", type=float, default=0.5)
    ap.add_argument("--peak_min_height", type=float, default=1.0)
    ap.add_argument("--char_window", type=float, default=0.5,
                    help="energy window (eV) below VBM / above CBM for orbital character")
    ap.add_argument("--xlim", type=float, nargs=2, default=[-15, 10])
    ap.add_argument("--title", default=None,
                    help="optional plot title (e.g., composition)")
    args = ap.parse_args()

    d = Path(args.dir)
    out_pref = args.out_prefix or args.prefix
    E, DOS, EF = read_total_dos(d / f"{args.prefix}_dos.dat")
    print(f"read total DOS: {len(E)} points, EF = {EF}")

    E_p, per_elem, per_elem_orb = read_pdos_files(d, args.prefix)
    for el, p in per_elem.items():
        print(f"  PDOS sum for {el}: integral = {np.trapezoid(p, E_p):.2f} states")

    vbm, cbm, gap = find_gap(E, DOS, EF, e_min=args.e_min, dos_thresh=args.dos_thresh)
    if vbm is None:
        print("no gap found"); return
    i_vbm = int(np.argmin(np.abs(E - vbm)))
    i_cbm = int(np.argmin(np.abs(E - cbm)))
    print(f"VBM={vbm:.3f} (DOS={DOS[i_vbm]:.3f})  "
          f"CBM={cbm:.3f} (DOS={DOS[i_cbm]:.3f})  gap={gap:.3f} eV")

    peaks = local_maxima(E, DOS, min_height=args.peak_min_height)
    vbm_peak_t = closest_peak_below(peaks, vbm)
    cbm_peak_t = closest_peak_above(peaks, cbm)
    if vbm_peak_t:
        print(f"  closest VBM peak: {vbm_peak_t[0]:.3f} eV (DOS={vbm_peak_t[1]:.2f})")
    if cbm_peak_t:
        print(f"  closest CBM peak: {cbm_peak_t[0]:.3f} eV (DOS={cbm_peak_t[1]:.2f})")

    vbm_break = character_at_edge(E_p, per_elem_orb, vbm,
                                   window=args.char_window, side="valence")
    cbm_break = character_at_edge(E_p, per_elem_orb, cbm,
                                   window=args.char_window, side="conduction")
    vbm_char = format_character(vbm_break)
    cbm_char = format_character(cbm_break)
    if vbm_char: print(f"  VBM character: {vbm_char}")
    if cbm_char: print(f"  CBM character: {cbm_char}")

    summary = {
        "EF_eV_qe": EF,
        "VBM_eV": vbm,
        "CBM_eV": cbm,
        "band_gap_eV": gap,
        "VBM_peak_eV": vbm_peak_t[0] if vbm_peak_t else None,
        "CBM_peak_eV": cbm_peak_t[0] if cbm_peak_t else None,
        "VBM_character": vbm_char,
        "CBM_character": cbm_char,
        "VBM_character_breakdown_pct": vbm_break,
        "CBM_character_breakdown_pct": cbm_break,
        "character_window_eV": args.char_window,
        "dos_threshold_states_per_eV": args.dos_thresh,
        "e_min_eV": args.e_min,
        "method": (
            f"VBM/CBM = edges of low-DOS run (DOS<{args.dos_thresh}, E>{args.e_min} eV) "
            f"straddling EF; peaks = nearest local maxima with height≥{args.peak_min_height}; "
            f"character = PDOS percent within {args.char_window} eV of edge."
        ),
    }
    json_path = d / f"{out_pref}_dos_summary.json"
    json_path.write_text(json.dumps(summary, indent=2))
    print(f"  → {json_path}")

    plot_raw(E, DOS, EF, vbm, cbm, vbm_peak_t, cbm_peak_t, gap,
             d / f"{out_pref}_dos_raw.png", xlim=tuple(args.xlim),
             title=args.title or "Total DOS")
    plot_pdos(E, DOS, EF, vbm, cbm, gap, E_p, per_elem,
              vbm_char, cbm_char,
              d / f"{out_pref}_dos_pdos.png", xlim=tuple(args.xlim),
              title=args.title)


if __name__ == "__main__":
    main()
