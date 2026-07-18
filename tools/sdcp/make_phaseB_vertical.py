#!/usr/bin/env python3
"""make_phaseB_vertical.py — CLEAN vertical (fixed-geometry) E_bind for doped SDCP.

WHY: the v2 molecule-only RELAX was flawed -- the doped radical DESORBS (moved to
4.48 A from the slab) and relaxes its internal geometry away from the fixed gas
reference, so E_bind drifted to a spurious -3.29 eV (internal relaxation, not
binding). The original Phase-B is single-point (both complex and gas mol at the
SAME molecular geometry) -> a clean VERTICAL binding energy. We restore that, but
at the image-clean SAME-POSE doped geometry (neutral relaxed pose minus the acidic
H) so it is directly comparable to the clean neutral value (-2.213 eV).

Emits two single-points from complex_neutral/scf.in (96 slab + 35 neutral mol):
  complex_doped_v2/scf.in : 221, tot_mag 1, all 130 atoms (neutral pose minus H)
  mol_doped_v2/scf.in     : gamma, vacuum box, tot_mag 1, the 34 molecule atoms only
k-sampling matches the existing clean references (complex 221, gas mol gamma), so
  E_bind(doped) = E(complex_doped_v2) - E_slab - E(mol_doped_v2)
  Delta = E_bind(doped) - E_bind(neutral=-2.213)   <- clean vertical doping effect.
NO relaxation. Cheap (2 SCF). Run after the (now-killed) relax.

Usage (gabia):  PHASEB_BASE=/data/work/runs/sdcp_linio2_binding/phaseB_v7c \
                python3 make_phaseB_vertical.py
"""
import os
import re

import numpy as np

BASE = os.environ.get("PHASEB_BASE", ".")
NSLAB = 96
VAC = 15.0  # A vacuum padding around the gas molecule

src = os.path.join(BASE, "complex_neutral", "scf.in")
txt = open(src).read()
lines = txt.splitlines()

# --- namelist header up to (not including) ATOMIC_POSITIONS, + cell + species ---
i0 = next(i for i, l in enumerate(lines) if l.strip().upper().startswith("ATOMIC_POSITIONS"))
atom_idx = [i for i in range(i0 + 1, len(lines))
            if re.match(r"^\s*[A-Za-z][a-z]?\d?\s+[-\d.]", lines[i])]
assert len(atom_idx) == 131, f"expected 131 atoms, got {len(atom_idx)}"
atoms = [(lines[i].split()[0], np.array([float(x) for x in lines[i].split()[1:4]])) for i in atom_idx]

# acidic H = molecule H within 1.15 A of a molecule O
mol = atoms[NSLAB:]
acid = [k for k, a in enumerate(mol) if a[0] == "H" and any(
    b[0] == "O" and np.linalg.norm(a[1] - b[1]) < 1.15 for b in mol)]
assert len(acid) == 1, f"acidic H ambiguous: {acid}"
doped_mol = [a for k, a in enumerate(mol) if k != acid[0]]      # 34 atoms
assert len(doped_mol) == 34

# ---------- 1) complex_doped_v2 : 221 single-point, minus H ----------
out = []
seen_pos = False
n_written = 0
drop_line = atom_idx[NSLAB + acid[0]]
for i, l in enumerate(lines):
    if i == drop_line:
        continue
    out.append(l)
ctxt = "\n".join(out) + "\n"
ctxt = ctxt.replace("nat             = 131", "nat             = 130")
ctxt = re.sub(r"prefix\s*=\s*'[^']*'", "prefix          = 'pb_cxd2v'", ctxt)
ctxt = ctxt.replace("tot_magnetization = 0.0", "tot_magnetization = 1.0")
# calculation stays 'scf' (single point), K_POINTS stays 2 2 1 -> identical to neutral
dst = os.path.join(BASE, "complex_doped_v2")
os.makedirs(dst, exist_ok=True)
open(os.path.join(dst, "scf.in"), "w").write(ctxt)
print(f"-> {dst}/scf.in  (130 at, 221 single-point, tot_mag 1, same-pose doped)")

# ---------- 2) mol_doped_v2 : gamma gas box, the 34 molecule atoms ----------
# pull &CONTROL/&SYSTEM/&ELECTRONS + ATOMIC_SPECIES from the source; drop HUBBARD,
# Ni species, magnetization lines; new orthorhombic box; gamma.
P = np.array([a[1] for a in doped_mol])
P = P - P.min(0) + VAC / 2
box = P.max(0) + VAC / 2
species = []
for a in doped_mol:
    if a[0] not in species:
        species.append(a[0])
# species pseudo lines from source ATOMIC_SPECIES
spec_block = {}
si = next(i for i, l in enumerate(lines) if l.strip().upper().startswith("ATOMIC_SPECIES"))
for l in lines[si + 1:]:
    s = l.split()
    if len(s) >= 3 and s[0] in ("Li", "Ni1", "Ni2", "O", "C", "H", "S"):
        spec_block[s[0]] = l
    elif l.strip() and not s[0][0].isalpha():
        break
    elif l.strip().upper().startswith(("HUBBARD", "CELL", "K_POINTS", "ATOMIC_POS")):
        break

m = ["&CONTROL", "    calculation     = 'scf'", "    prefix          = 'pb_mold2v'",
     "    outdir          = './tmp'", "    pseudo_dir      = '/data/work/pseudo'",
     "    tprnfor         = .true.", "    disk_io         = 'low'", "/",
     "&SYSTEM", "    ibrav           = 0", f"    nat             = {len(doped_mol)}",
     f"    ntyp            = {len(species)}", "    ecutwfc         = 60.0",
     "    ecutrho         = 480.0", "    occupations     = 'smearing'",
     "    smearing        = 'mv'", "    degauss         = 0.02", "    nspin           = 2",
     "    tot_magnetization = 1.0", "    starting_magnetization(1) = 0.1", "/",
     "&ELECTRONS", "    conv_thr        = 1e-06", "    mixing_beta     = 0.3", "/", "",
     "ATOMIC_SPECIES"]
for sp in species:
    m.append(spec_block[sp])
m += ["", "CELL_PARAMETERS angstrom",
      f"  {box[0]:14.8f}   0.00000000   0.00000000",
      f"   0.00000000  {box[1]:14.8f}   0.00000000",
      f"   0.00000000   0.00000000  {box[2]:14.8f}", "",
      "K_POINTS gamma", "", "ATOMIC_POSITIONS angstrom"]
for a, p in zip(doped_mol, P):
    m.append(f"  {a[0]:3s} {p[0]:16.10f} {p[1]:16.10f} {p[2]:16.10f}")
dstm = os.path.join(BASE, "mol_doped_v2")
os.makedirs(dstm, exist_ok=True)
open(os.path.join(dstm, "scf.in"), "w").write("\n".join(m) + "\n")
print(f"-> {dstm}/scf.in  (34 at gas box {box.round(1)}, gamma, tot_mag 1, matched geometry)")
print("run both SCFs, then:")
print("  E_bind(doped) = E(complex_doped_v2) - E_slab(-10563.22819091) - E(mol_doped_v2)")
print("  compare to E_bind(neutral) = -2.213 eV (clean). Delta = vertical doping effect.")
