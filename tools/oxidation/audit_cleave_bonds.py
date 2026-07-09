#!/usr/bin/env python3
"""audit_cleave_bonds.py — cleave-integrity audit for roll_c interface builds.

The roll+cleave in build_li_interface.py breaks c-periodicity: any bond that
crossed the (rolled) cell's c-boundary is physically severed in the slab. A
severed front-line unit is hyper-reactive and its instant decomposition in MD
is a BUILD ARTIFACT, not chemistry (lesson: b2o3 roll 0.16 exposed a P whose
3 S were cut -> "P-O destroyed within equilibration" had to be retracted).

RUN THIS BEFORE EVERY roll_c MD LAUNCH. Launch only if the contact zone shows
no SEVERED flags.

  # audit one roll
  python3 audit_cleave_bonds.py --structure db/structures/b2o3_relaxV0.xyz --roll 0.71
  # scan all rolls for clean O-exposed windows (O outermost, parent cage intact)
  python3 audit_cleave_bonds.py --structure db/structures/b2o3_relaxV0.xyz --scan
"""
import argparse
import numpy as np
from ase.io import read

CUT = {("P", "S"): 2.6, ("P", "O"): 2.0, ("B", "S"): 2.4, ("B", "O"): 2.0}
CUT.update({(b, a): r for (a, b), r in list(CUT.items())})   # symmetric lookup


def neighbors(atoms, i, pbc_c):
    """bonded neighbors of atom i; pbc_c=False = slab (cleaved along c)."""
    sym = atoms.get_chemical_symbols()
    cell = atoms.cell.array
    out = []
    for j in range(len(atoms)):
        if j == i or (sym[i], sym[j]) not in CUT:
            continue
        f = np.linalg.solve(cell.T, atoms.positions[j] - atoms.positions[i])
        w = np.round(f)
        if not pbc_c:
            w[2] = 0.0
        r = np.linalg.norm((f - w) @ cell)
        if r < CUT[(sym[i], sym[j])]:
            out.append((j, sym[j], round(float(r), 2)))
    return out


def rolled(bulk, roll):
    se = bulk.copy()
    f = se.get_scaled_positions()
    f[:, 2] = (f[:, 2] + roll) % 1.0
    se.set_scaled_positions(f)
    return se


def audit(bulk, roll, zwin=9.0, verbose=True):
    se = rolled(bulk, roll)
    sym = np.array(se.get_chemical_symbols())
    z = se.positions[:, 2]
    zmax = z.max()
    n_severed = 0
    for el in ("O", "B", "P"):
        for i in sorted(np.where(sym == el)[0], key=lambda k: zmax - z[k]):
            d = zmax - z[i]
            if d > zwin:
                continue
            nb_b = neighbors(se, i, True)
            nb_s = neighbors(se, i, False)
            sev = len(nb_b) - len(nb_s)
            n_severed += sev
            if verbose:
                fb = " ".join(f"{s}{r}" for _, s, r in nb_b)
                fs = " ".join(f"{s}{r}" for _, s, r in nb_s)
                print(f" {el} depth={d:4.1f} A  bulk={len(nb_b)} [{fb}]  slab={len(nb_s)} [{fs}]"
                      + (f"   <-- CLEAVE SEVERED {sev}" if sev else ""))
    if verbose:
        print(("!! DO NOT LAUNCH — cleave-damaged unit(s) in the contact zone"
               if n_severed else "OK — contact zone intact, safe to launch"))
    return n_severed


def scan(bulk):
    sym = np.array(bulk.get_chemical_symbols())
    print("roll  O_depth  parentP_depth  cage  top8_severed  verdict")
    clean = []
    for roll in np.arange(0.0, 1.0, 0.01):
        se = rolled(bulk, roll)
        z = se.positions[:, 2]
        zmax = z.max()
        Os = [i for i in np.where(sym == "O")[0] if zmax - z[i] < 3.0]
        if not Os:
            continue
        oi = min(Os, key=lambda i: zmax - z[i])
        ps = [j for j, s, _ in neighbors(se, oi, False) if s in ("P", "B")]
        if not ps:
            continue
        pi = ps[0]
        cage_s, cage_b = len(neighbors(se, pi, False)), len(neighbors(se, pi, True))
        sev = sum(1 for k in range(len(se))
                  if sym[k] in ("P", "B") and zmax - z[k] < 8.0
                  and len(neighbors(se, k, True)) != len(neighbors(se, k, False)))
        ok = cage_s == cage_b and sev == 0 and (zmax - z[oi]) < (zmax - z[pi])
        if cage_s == cage_b and sev == 0:
            print(f"{roll:.2f}  {zmax-z[oi]:5.1f}    {zmax-z[pi]:5.1f}        {cage_s}/{cage_b}    {sev}"
                  + ("     *** CLEAN O-up ***" if ok else "     clean, O not outermost"))
        if ok:
            clean.append(round(float(roll), 2))
    print("\nCLEAN O-up rolls:", clean)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--structure", required=True)
    ap.add_argument("--roll", type=float, default=None)
    ap.add_argument("--scan", action="store_true")
    ap.add_argument("--zwin", type=float, default=9.0, help="audit window below the exposed top (A)")
    a = ap.parse_args()
    bulk = read(a.structure)
    if a.scan:
        scan(bulk)
    if a.roll is not None:
        print(f"=== {a.structure}  roll_c={a.roll} ===")
        audit(bulk, a.roll, a.zwin)


if __name__ == "__main__":
    main()
