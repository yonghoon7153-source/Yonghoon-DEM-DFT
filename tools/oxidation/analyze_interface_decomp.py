#!/usr/bin/env python3
"""analyze_interface_decomp.py — decomposition metrics from an SE|Li interface traj.

Tracks, per production frame, the fingerprints of Li reducing the SE:
  - P-S coordination   (intact PS4 ~ 4 ; drop = P-S bond breaking -> PS_n)
  - S-Li coordination  (rise = Li2S_n formation on S)
  - P-Li coordination  (rise = Li3P formation on P)
  - B-S / B-Li         (b2o3 only: BS3 ~3 ; B-Li>0 = metallic LiB reduction  <-- THE flag)
  - Li penetration     (# Li that crossed below the initial SE surface)
Writes a per-frame CSV + an initial-vs-final summary. Run per system, then compare
b2o3 vs modelc (more P-S loss / Li penetration / B-Li = worse dynamic decomposition).

  python3 tools/oxidation/analyze_interface_decomp.py b2o3_traj.xyz --label b2o3 \
    --dt_ps 0.2 --out db/properties/interface_decomp_b2o3.csv
"""
import argparse
import numpy as np
from ase.io import read

CUT = {("P", "S"): 2.6, ("B", "S"): 2.5, ("B", "O"): 1.9, ("P", "O"): 1.9,
       ("Li", "S"): 2.95, ("Li", "P"): 2.9, ("Li", "B"): 2.85, ("Li", "Cl"): 3.0,
       ("Li", "O"): 2.4}


def coord(atoms, D, sym, a, b, cut):
    ia = np.where(sym == a)[0]
    ib = np.where(sym == b)[0]
    if len(ia) == 0 or len(ib) == 0:
        return np.nan
    sub = D[np.ix_(ia, ib)]
    return float((sub < cut).sum(axis=1).mean())     # avg # of b-neighbors per a


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("traj")
    ap.add_argument("--label", required=True)
    ap.add_argument("--dt_ps", type=float, default=0.2, help="save interval (ps) between frames")
    ap.add_argument("--out", default=None)
    a = ap.parse_args()

    frames = read(a.traj, index=":")
    sym0 = np.array(frames[0].get_chemical_symbols())
    has_B = "B" in sym0
    # O dopant present AND not part of B2O3 (b2o3 O is tracked via B); for LPSOCl the O
    # is a POS3 unit -> track P-O (unit intact) and O-Li (O reduced to Li2O). 2026-07-18.
    has_O = ("O" in sym0) and not has_B

    se_top0 = frames[0].positions[sym0 != "Li", 2].max()   # initial SE surface z

    rows = []
    hdr = ["frame", "t_ps", "P_S", "S_Li", "P_Li", "Li_penetrated"]
    if has_B:
        hdr += ["B_S", "B_Li"]
    if has_O:
        hdr += ["P_O", "O_Li"]
    for k, at in enumerate(frames):
        sym = np.array(at.get_chemical_symbols())
        D = at.get_all_distances(mic=True)
        r = [k, k * a.dt_ps,
             coord(at, D, sym, "P", "S", CUT[("P", "S")]),
             coord(at, D, sym, "S", "Li", CUT[("Li", "S")]),
             coord(at, D, sym, "P", "Li", CUT[("Li", "P")])]
        # Li that crossed below the initial SE surface (penetration into SE)
        zli = at.positions[sym == "Li", 2]
        r.append(int((zli < se_top0).sum()))
        if has_B:
            r.append(coord(at, D, sym, "B", "S", CUT[("B", "S")]))
            r.append(coord(at, D, sym, "B", "Li", CUT[("Li", "B")]))
        if has_O:
            # from O's view: O-P ~1 = POS3 intact (drop = P-O broke); O-Li rise = Li2O
            r.append(coord(at, D, sym, "O", "P", CUT[("P", "O")]))
            r.append(coord(at, D, sym, "O", "Li", CUT[("Li", "O")]))
        rows.append(r)

    rows = np.array(rows, float)
    out = a.out or f"interface_decomp_{a.label}.csv"
    with open(out, "w") as f:
        f.write(",".join(hdr) + "\n")
        for row in rows:
            f.write(",".join(f"{v:.3f}" for v in row) + "\n")

    i0, iN = rows[0], rows[-1]
    ps4_loss = (i0[2] - iN[2]) / i0[2] * 100 if i0[2] else 0
    print(f"\n===== [{a.label}] interface decomposition ({len(frames)} frames, {rows[-1,1]:.0f} ps) =====")
    print(f"  P-S coord : {i0[2]:.2f} -> {iN[2]:.2f}   ({ps4_loss:+.0f}% PS4 bonds; drop = P-S breaking)")
    print(f"  S-Li coord: {i0[3]:.2f} -> {iN[3]:.2f}   (rise = Li2S_n on S)")
    print(f"  P-Li coord: {i0[4]:.2f} -> {iN[4]:.2f}   (rise = Li3P on P)")
    print(f"  Li penetr.: {int(i0[5])} -> {int(iN[5])} atoms below initial SE surface")
    if has_B:
        print(f"  B-S coord : {i0[6]:.2f} -> {iN[6]:.2f}   (BS3 ~3; drop = B-S breaking)")
        print(f"  B-Li coord: {i0[7]:.2f} -> {iN[7]:.2f}   <-- >0 = metallic-LiB reduction (THE worst-case flag)")
    if has_O:
        print(f"  P-O coord : {i0[6]:.2f} -> {iN[6]:.2f}   (O-P ~1 = POS3 intact; drop = P-O breaking)")
        print(f"  O-Li coord: {i0[7]:.2f} -> {iN[7]:.2f}   <-- rise = O reduced to Li2O (the O-dopant flag)")
    print(f"  -> {out}")


if __name__ == "__main__":
    main()
