#!/usr/bin/env python3
"""b2o3_eos_fit.py — BM3 fit of the B2O3-doped DFT EOS -> doped B0 vs modelC 21.7.
Run in the dir holding eos_v*.out (after the KISTI EOS volumes reach JOB DONE):
    python3 b2o3_eos_fit.py
Only JOB-DONE volumes are used; needs >=4 points.
"""
import glob, re
from ase.eos import EquationOfState
from ase.units import kJ

VE = []
for o in sorted(glob.glob("eos_v*.out")):
    t = open(o).read()
    if "JOB DONE" not in t:
        continue
    m = re.findall(r"!\s+total energy\s+=\s+(-?\d+\.\d+)", t)   # Ry
    v = re.findall(r"unit-cell volume\s*=\s*([\d.]+)", t)       # bohr^3
    if m and v:
        VE.append((float(v[-1]) * 0.148184, float(m[-1]) * 13.605693))  # ->A^3, ->eV

if len(VE) >= 4:
    VE.sort()
    V = [x[0] for x in VE]
    E = [x[1] for x in VE]
    eos = EquationOfState(V, E, eos="birchmurnaghan")
    v0, e0, B = eos.fit()
    B0 = B / kJ * 1e24
    print(f"BM3: n={len(VE)}  V0={v0:.1f} A3  B0={B0:.1f} GPa  (modelC DFT 21.7 -> dB0={B0-21.7:+.1f})")
else:
    print(f"only {len(VE)} JOB DONE pts — need >=4")
