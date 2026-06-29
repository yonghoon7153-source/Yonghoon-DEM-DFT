#!/usr/bin/env python3
"""Sum projwfc per-atom PDOS into one compact CSV (total + element-projected).

Avoids transferring the hundreds of b2o3.pdos.pdos_atm#*_wfc#* files: run this
ON the cluster where projwfc ran, get ONE CSV, transfer that.

Columns: E_eV, E_minus_Ef, total_dos, <one column per element>.
Element PDOS = sum of the LDOS column (col 2) over every wfc file of that element.
E_Fermi read from the <prefix>.dos header (dos.x); falls back to --vbm.

  python3 sum_pdos.py --dir /scratch/.../b2o3_eos --prefix b2o3 \
      --out /scratch/.../b2o3_eos/b2o3_dos_pdos.csv
"""
import argparse, glob, re, csv
import numpy as np


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", required=True)
    ap.add_argument("--prefix", default="b2o3")
    ap.add_argument("--out", default=None)
    ap.add_argument("--vbm", type=float, default=2.4717,
                    help="fallback E shift (VBM) if no EFermi in .dos header")
    args = ap.parse_args()
    d, p = args.dir.rstrip("/"), args.prefix
    out = args.out or f"{d}/{p}_dos_pdos.csv"

    tot = np.loadtxt(f"{d}/{p}.pdos.pdos_tot")
    E = tot[:, 0]
    total_dos = tot[:, 1]                      # col2 = total DOS

    Ef = None
    try:
        with open(f"{d}/{p}.dos") as f:
            h = f.readline()
        m = re.search(r"EFermi\s*=\s*(-?[\d.]+)", h)
        if m:
            Ef = float(m.group(1))
    except FileNotFoundError:
        pass
    if Ef is None:
        Ef = args.vbm
        print(f"[warn] no EFermi in {p}.dos header -> using VBM {Ef}")

    files = glob.glob(f"{d}/{p}.pdos.pdos_atm#*_wfc#*")
    els, sums = [], {}
    for fn in files:
        m = re.search(r"pdos_atm#\d+\((\w+)\)_wfc#", fn)
        if not m:
            continue
        el = m.group(1)
        arr = np.loadtxt(fn)
        if el not in sums:
            sums[el] = np.zeros_like(E); els.append(el)
        sums[el] += arr[:, 1]                  # LDOS column
    els = sorted(els, key=lambda e: {"Li":0,"P":1,"S":2,"Cl":3,"B":4,"O":5}.get(e, 9))
    print(f"Ef={Ef:.4f} eV  E grid={len(E)} pts  elements={els}  ({len(files)} wfc files)")

    with open(out, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["E_eV", "E_minus_Ef", "total_dos"] + els)
        for i in range(len(E)):
            w.writerow([f"{E[i]:.4f}", f"{E[i]-Ef:.4f}", f"{total_dos[i]:.5f}"] +
                       [f"{sums[el][i]:.5f}" for el in els])
    print(f"-> {out}")


if __name__ == "__main__":
    main()
