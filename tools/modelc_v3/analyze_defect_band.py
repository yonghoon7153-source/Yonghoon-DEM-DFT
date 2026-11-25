#!/usr/bin/env python3
"""Per-atom analysis of PDOS in a chosen energy window — used to identify
which specific atoms contribute to a defect band (e.g., Li-vacancy-induced
states near EF in modelc_v3, between EF and VBM).

Reads V0_pdos.pdos_atm#N(El)_wfc#M(L) files, integrates each atom's PDOS
in the user-specified window, sorts by contribution, and outputs:
  - top contributors per element
  - JSON breakdown

Usage example (modelc EF=2.445, VBM=2.72 → defect band window [2.445, 2.72]):
    python3 analyze_defect_band.py --dir /home/ubuntu/work/runs/modelC_v3 \\
        --prefix V0 --e_lo 2.445 --e_hi 2.72 \\
        --label "defect band between EF and VBM" \\
        --out V0_defect_band_analysis.json
"""
import argparse
import json
import re
from pathlib import Path
import numpy as np


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", required=True)
    ap.add_argument("--prefix", default="V0")
    ap.add_argument("--e_lo", type=float, required=True)
    ap.add_argument("--e_hi", type=float, required=True)
    ap.add_argument("--label", default="user-specified window")
    ap.add_argument("--out", default=None)
    ap.add_argument("--top_n", type=int, default=10)
    args = ap.parse_args()

    d = Path(args.dir)
    pat = re.compile(rf"{re.escape(args.prefix)}_pdos\.pdos_atm#(\d+)\(([A-Za-z]+)\)_wfc#(\d+)\(([a-z])\)$")

    # atom_idx -> {"element": str, "orbitals": {orb: integral}}
    per_atom = {}
    for fp in sorted(d.iterdir()):
        m = pat.match(fp.name)
        if not m:
            continue
        atom_idx, elem, wfc_idx, orb = m.groups()
        atom_idx = int(atom_idx)
        data = np.loadtxt(fp, comments="#")
        E = data[:, 0]
        ldos = data[:, 1]
        mask = (E >= args.e_lo) & (E <= args.e_hi)
        if not mask.any():
            integral = 0.0
        else:
            integral = float(np.trapezoid(ldos[mask], E[mask]))
        per_atom.setdefault(atom_idx, {"element": elem, "orbitals": {}, "total": 0.0})
        per_atom[atom_idx]["orbitals"][orb] = per_atom[atom_idx]["orbitals"].get(orb, 0.0) + integral
        per_atom[atom_idx]["total"] += integral

    # Sum per element + per (element, orbital)
    per_elem = {}
    per_elem_orb = {}
    for ai, info in per_atom.items():
        el = info["element"]
        per_elem.setdefault(el, 0.0)
        per_elem[el] += info["total"]
        for orb, v in info["orbitals"].items():
            per_elem_orb.setdefault((el, orb), 0.0)
            per_elem_orb[(el, orb)] += v

    total = sum(per_elem.values())
    print(f"=== Window: [{args.e_lo}, {args.e_hi}] eV ({args.label}) ===")
    print(f"Total integrated PDOS: {total:.4f} states")
    if total <= 0:
        print("  empty window")
        return

    print(f"\nPer-element contribution:")
    elem_pct = {}
    for el, v in sorted(per_elem.items(), key=lambda x: -x[1]):
        pct = 100 * v / total
        elem_pct[el] = pct
        print(f"  {el}: {v:.4f} states ({pct:.1f}%)")

    print(f"\nPer-(element, orbital) contribution:")
    eo_pct = {}
    for (el, orb), v in sorted(per_elem_orb.items(), key=lambda x: -x[1]):
        pct = 100 * v / total
        eo_pct[f"{el}_{orb}"] = pct
        print(f"  {el} {orb}: {v:.4f} states ({pct:.1f}%)")

    print(f"\nTop-{args.top_n} individual atoms:")
    sorted_atoms = sorted(per_atom.items(), key=lambda x: -x[1]["total"])
    top_atoms = []
    for ai, info in sorted_atoms[:args.top_n]:
        orbs = ", ".join(f"{o}={v:.4f}" for o, v in
                          sorted(info["orbitals"].items(), key=lambda x: -x[1]))
        pct = 100 * info["total"] / total
        print(f"  atom #{ai} ({info['element']}): {info['total']:.4f} states ({pct:.2f}%) — {orbs}")
        top_atoms.append({
            "atom_index": ai,
            "element": info["element"],
            "integrated_states": round(info["total"], 5),
            "percent_of_window": round(pct, 2),
            "by_orbital": {k: round(v, 5) for k, v in info["orbitals"].items()},
        })

    out = {
        "window_eV": [args.e_lo, args.e_hi],
        "label": args.label,
        "total_states_in_window": round(total, 4),
        "per_element_percent": {k: round(v, 2) for k, v in elem_pct.items()},
        "per_element_orbital_percent": {k: round(v, 2) for k, v in eo_pct.items()},
        "top_atoms": top_atoms,
    }
    if args.out:
        Path(args.dir, args.out).write_text(json.dumps(out, indent=2))
        print(f"\n  → {Path(args.dir, args.out)}")


if __name__ == "__main__":
    main()
