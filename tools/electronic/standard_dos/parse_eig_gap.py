#!/usr/bin/env python3
"""Standard eigenvalue band gap from a QE pw.x (n)scf output.

The gap = CBM - VBM read straight from the Kohn-Sham eigenvalues (VBM = highest
eigenvalue <= E_F, CBM = lowest eigenvalue > E_F). This is the literature
convention (VASP/QE band-structure gap) and is INDEPENDENT of the smearing used
(smearing only sets occupations / E_F, not the eigenvalues). It therefore fixes
the old 'DOS<0.5 threshold' underestimate WITHOUT re-running anything -- just
re-parse the existing nscf .out. Handles nspin=2 (collects both spin channels).

Usage:  python3 parse_eig_gap.py <nscf.out>
"""
import re
import sys
import numpy as np

L = open(sys.argv[1]).read().splitlines()
EF = [float(re.search(r'Fermi energy is\s*([-\d.]+)', x).group(1)) for x in L if 'Fermi energy is' in x]
if not EF:
    sys.exit("No 'Fermi energy' line — is this an scf/nscf output?")
EF = EF[-1]

eig, st = [], 0
for x in L:
    if 'bands (ev)' in x:
        st = 1; continue
    if st == 1:
        if x.strip() == '':
            continue
        st = 2
    if st == 2:
        t = x.split()
        if t and all(re.fullmatch(r'-?\d+\.\d+', k) for k in t):
            eig += [float(k) for k in t]
        else:
            st = 0

e = np.array(eig)
vbm = e[e <= EF].max()
cbm = e[e > EF].min()
print(f"EF  = {EF:.4f} eV   (n_eig = {len(e)})")
print(f"VBM = {vbm:.4f} eV")
print(f"CBM = {cbm:.4f} eV")
print(f"GAP = {cbm - vbm:.4f} eV   <-- eigenvalue gap (literature convention)")
