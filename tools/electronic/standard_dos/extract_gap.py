#!/usr/bin/env python3
"""Standard band gap from a QE pw.x output run with occupations='fixed'.
QE then prints 'highest occupied, lowest unoccupied level (ev): VBM CBM' and the
gap is CBM - VBM (eigenvalue/band-structure gap = the literature convention).

Usage:  python3 extract_gap.py nscf_gap.out
"""
import sys
import re

txt = open(sys.argv[1]).read()

m = re.search(r"highest occupied, lowest unoccupied level \(ev\):\s*([-\d.]+)\s+([-\d.]+)", txt)
if m:
    vbm, cbm = float(m.group(1)), float(m.group(2))
    print(f"  VBM = {vbm:.4f} eV")
    print(f"  CBM = {cbm:.4f} eV")
    print(f"  GAP = {cbm - vbm:.4f} eV   <-- eigenvalue (band-structure) gap, literature convention")
    sys.exit(0)

m2 = re.search(r"highest occupied level \(ev\):\s*([-\d.]+)", txt)
if m2:
    print(f"  highest occupied level = {float(m2.group(1)):.4f} eV  (no LUMO line)")
    print("  !! Raise nbnd (need empty bands), OR system has partial occupation")
    print("     (disorder defect band / EF<VBM) -> inspect the tetrahedron DOS.")
    sys.exit(0)

ef = re.search(r"the Fermi energy is\s*([-\d.]+)", txt)
print("  No insulator HOMO/LUMO line found.")
if ef:
    print(f"  Fermi energy = {float(ef.group(1)):.4f} eV  -> you used smearing; rerun with occupations='fixed'.")
