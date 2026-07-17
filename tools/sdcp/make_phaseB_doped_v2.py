#!/usr/bin/env python3
"""make_phaseB_doped_v2.py — SAME-POSE doped relax input (Phase-B v2, 2026-07-17).

WHY v2: the v1 doped complex (UMA champion chelation_r90) stands the molecule
vertically; its thiophene S ends 1.506 A from the PERIODIC IMAGE slab's O —
a bonding distance. v1 doped E_bind (-1.524 eV) is therefore an image-sandwich
artifact, RETRACTED. The neutral pose lies down (image gap 4.72 A, healthy).

DESIGN: take the healthy NEUTRAL complex geometry and delete the acidic SO3H
proton -> the doped radical (C11H15O6S2, 34 at) in the SAME lying pose, with
its sulfonate O already at the surface (chelation-ready). This is the clean
same-pose comparison AND it inherits the healthy vacuum. Gas ref unchanged
(mol_doped is exactly this stoichiometry).

Emits <PB>/complex_doped_v2/relax.in: molecule-only free (96 slab frozen),
gamma-point geometry pass, nstep 30, conv 1e-5 + scf_must_converge=.false.,
tot_magnetization 1.0 (doublet). Rescore at 221 afterwards.

Usage (gabia):  PHASEB_BASE=/data/work/runs/sdcp_linio2_binding/phaseB_v7c \
                python3 make_phaseB_doped_v2.py
"""
import os
import re

import numpy as np

BASE = os.environ.get("PHASEB_BASE", ".")
NSLAB = 96

src = os.path.join(BASE, "complex_neutral", "scf.in")
txt = open(src).read()
lines = txt.splitlines()

# --- collect atom lines ---
i0 = next(i for i, l in enumerate(lines) if l.strip().upper().startswith("ATOMIC_POSITIONS"))
atom_idx = [i for i in range(i0 + 1, len(lines))
            if re.match(r"^\s*[A-Z][a-z]?\d?\s+[-\d.]", lines[i])]
assert len(atom_idx) == 131, f"expected 131 atoms, got {len(atom_idx)}"
atoms = [(lines[i].split()[0], np.array([float(x) for x in lines[i].split()[1:4]]), i)
         for i in atom_idx]

# --- find the acidic H: molecule H within 1.15 A of a molecule O ---
mol = atoms[NSLAB:]
acid = [a for a in mol if a[0] == "H" and any(
    b[0] == "O" and np.linalg.norm(a[1] - b[1]) < 1.15 for b in mol)]
assert len(acid) == 1, f"acidic H ambiguous: {[(a[0], a[1].round(3)) for a in acid]}"
drop_line = acid[0][2]
print(f"acidic H found at {acid[0][1].round(3)} (O-H {min(np.linalg.norm(acid[0][1]-b[1]) for b in mol if b[0]=='O'):.3f} A) -> removed")

# --- rebuild input ---
out = []
for i, l in enumerate(lines):
    if i == drop_line:
        continue
    out.append(l)
txt = "\n".join(out) + "\n"
txt = txt.replace("nat             = 131", "nat             = 130")
txt = re.sub(r"prefix\s*=\s*'[^']*'", "prefix          = 'pb_cxd2'", txt)
txt = txt.replace("calculation     = 'scf'", "calculation     = 'relax'")
txt = txt.replace("outdir          = './tmp'", "outdir          = './tmp_relax'")
txt = txt.replace("disk_io         = 'low'", "disk_io         = 'low'\n    nstep           = 30")
txt = txt.replace("tot_magnetization = 0.0", "tot_magnetization = 1.0")
txt = txt.replace("conv_thr        = 1e-06", "conv_thr        = 1e-05")
txt = re.sub(r"(?m)^(&ELECTRONS[^\n]*\n)", r"\1    scf_must_converge = .false.\n", txt, count=1)
txt = re.sub(r"K_POINTS\s+automatic\s*\n\s*2 2 1 0 0 0", "K_POINTS gamma", txt)
txt = re.sub(r"(?m)^ATOMIC_SPECIES",
             "&IONS\n    ion_dynamics    = 'bfgs'\n/\n\nATOMIC_SPECIES", txt, count=1)

# freeze the slab (first NSLAB coordinate lines)
lines = txt.splitlines()
out, n = [], 0
seen = False
for l in lines:
    if l.strip().upper().startswith("ATOMIC_POSITIONS"):
        seen = True
        out.append(l)
        continue
    if seen and n < NSLAB and re.match(r"^\s*[A-Z][a-z]?\d?\s+[-\d.]", l):
        out.append(l + "   0 0 0")
        n += 1
        continue
    out.append(l)
assert n == NSLAB
dst_dir = os.path.join(BASE, "complex_doped_v2")
os.makedirs(dst_dir, exist_ok=True)
open(os.path.join(dst_dir, "relax.in"), "w").write("\n".join(out) + "\n")
print(f"-> {dst_dir}/relax.in  (130 at, same-pose doped, gamma relax, slab frozen)")
print("E_bind(v2) = E(final) - E_slab - E_mol_doped  [gas refs unchanged]")
