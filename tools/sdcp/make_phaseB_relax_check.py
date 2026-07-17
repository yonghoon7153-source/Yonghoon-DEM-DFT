#!/usr/bin/env python3
"""make_phaseB_relax_check.py — Phase-B VERDICT robustness check inputs (gabia).

Question (2026-07-17): is Delta(d-n) = +0.689 eV an artifact of the single-point
protocol (DFT never relaxed the UMA champion geometries)? Evidence that motivates
the check: in the DFT-scored doped pose the closest slab-molecule contact is
Ni...H 2.57 A (no O-surface bond at all), while neutral has real Ni-O contacts
at 1.94/2.31 A. If DFT+U relaxation lets the doped molecule descend/rotate into
a bonded pose, E_bind(doped) may recover part of the 0.689 eV.

Protocol: molecule-only relax (all 96 slab atoms if_pos 0 0 0) so the slab
reference stays IDENTICAL in complex and bare slab -> E_bind formula unchanged,
systematics cancel as before. Everything else (U, AFM, smearing, local-TF
mixing, cutoffs) cloned verbatim from the converged phaseB scf.in.

Usage (on gabia):
  cd /data/work/runs/sdcp_linio2_binding/phaseB_v7c
  python3 ~/work/Yonghoon-DEM-DFT/tools/sdcp/make_phaseB_relax_check.py
Writes complex_doped/relax.in and complex_neutral/relax.in (nstep 80, BFGS,
QE-default conv: etot 1e-4 Ry, forc 1e-3 Ry/bohr).
"""
import os
import re

BASE = os.environ.get("PHASEB_BASE", ".")
NSLAB = 96

for tag in ("complex_doped", "complex_neutral"):
    src = os.path.join(BASE, tag, "scf.in")
    txt = open(src).read()
    txt = txt.replace("calculation     = 'scf'",
                      "calculation     = 'relax'")
    txt = txt.replace("outdir          = './tmp'",
                      "outdir          = './tmp_relax'")
    txt = re.sub(r"prefix          = '([^']*)'",
                 lambda m: f"prefix          = '{m.group(1)}_rlx'", txt)
    # forces already on (tprnfor); add nstep + IONS block before &SYSTEM? no — CONTROL gets nstep
    txt = txt.replace("disk_io         = 'low'",
                      "disk_io         = 'low'\n    nstep           = 30")
    # relax survival (2026-07-17): these complexes historically PLATEAU near 1e-5..1e-6
    # (neutral: 272 iters -> acc 7.6e-6) and pw.x ABORTS a relax on a non-converged step.
    # 1e-5 is plenty for BFGS forces at 1e-3 au; scf_must_converge keeps a stubborn
    # step from killing the whole chain.
    txt = txt.replace("conv_thr        = 1e-06", "conv_thr        = 1e-05")
    txt = re.sub(r"(?m)^(&ELECTRONS[^\n]*\n)", r"\1    scf_must_converge = .false.\n", txt, count=1)
    # SPEED (2026-07-17): geometry pass at a single Gamma k-point via a 1x1x1 MESH
    # (4x fewer k-points than 221@nosym). NOT "K_POINTS gamma" — QE's gamma-only
    # real-wfc code path aborts with "Gamma-only calculation for this case not
    # implemented" for this input combo (HUBBARD ortho-atomic / FSM); the 1x1x1
    # mesh samples the same Gamma point through the standard complex-wfc path.
    # FINAL energies = 221 single-point RESCORE on the relaxed geometry.
    txt = re.sub(r"K_POINTS\s+automatic\s*\n\s*2 2 1 0 0 0",
                 "K_POINTS automatic\n  1 1 1 0 0 0", txt)
    # namelist order must be CONTROL/SYSTEM/ELECTRONS/IONS -> insert IONS after ELECTRONS
    txt = re.sub(r"(?m)^ATOMIC_SPECIES",
                 "&IONS\n    ion_dynamics    = 'bfgs'\n/\n\nATOMIC_SPECIES", txt, count=1)
    # freeze the slab: append '0 0 0' to the first NSLAB coordinate lines
    lines = txt.splitlines()
    out, n_in_pos, seen = [], 0, False
    for ln in lines:
        if ln.strip().upper().startswith("ATOMIC_POSITIONS"):
            seen = True
            out.append(ln)
            continue
        if seen and n_in_pos < NSLAB and re.match(r"^\s*[A-Z][a-z]?\d?\s+[-\d.]", ln):
            out.append(ln + "   0 0 0")
            n_in_pos += 1
            continue
        out.append(ln)
    assert n_in_pos == NSLAB, f"{tag}: froze {n_in_pos} != {NSLAB}"
    dst = os.path.join(BASE, tag, "relax.in")
    open(dst, "w").write("\n".join(out) + "\n")
    print(f"{dst}: relax, molecule-only free (slab {NSLAB} frozen), nstep 30, gamma")
print("run order: doped first (the suspect pose), then neutral (fairness).")
print("E_bind(relaxed) = E(complex relax final) - E_slab - E_mol  (refs unchanged)")
