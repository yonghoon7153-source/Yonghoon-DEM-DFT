#!/usr/bin/env python3
"""make_qe_inputs.py — wrap periodic slab structures (periodic/*.qe) in full QE
inputs for the h-BN@VGCF Li-adsorption study.

PARAMS PINNED from the two digests (both periodic-slab PBE):
  Shi 2017 (ACS AMI 2017, Quantum ESPRESSO -- OUR toolchain): PBE, PAW, D2
    (we use D3-BJ, modern), ecutwfc ~78 Ry, k-spacing < 0.05/A, force 0.01 eV/A,
    vacuum 10-15 A, E_ads = E(surf+Li) - E(surf) - E(Li atom)  [isolated-atom ref].
    Bare h-BN Li adsorption target: hollow -0.56 / N-top -0.46 eV; diffusion 0.10 eV.
  Liu 2022 (VASP): PBE 500 eV, no vdW; Li deposits BETWEEN h-BN and the bottom layer
    (sandwich strongest). Bottom = Cu(-2.50). OURS = VGCF (graphene, weak) -> the test.

E_ads reference = isolated Li atom (matches both papers). Bulk-Li conversion
(cohesive ~1.63 eV/atom) for true lithiophobicity is done in analysis, not here.
Emits qe_inputs/*.in (relax) + Li_atom.in reference. Pseudos: PSlibrary PBE kjpaw PAW.
"""
import glob
import os
import re

PSEUDO = {"C": "C.pbe-n-kjpaw_psl.1.0.0.UPF", "B": "B.pbe-n-kjpaw_psl.1.0.0.UPF",
          "N": "N.pbe-n-kjpaw_psl.1.0.0.UPF", "Li": "Li.pbe-s-kjpaw_psl.1.0.0.UPF"}
MASS = {"C": 12.011, "B": 10.811, "N": 14.007, "Li": 6.941}
ECUTWFC, ECUTRHO = 60.0, 480.0      # PAW; Shi used 78 Ry (raise if convergence needs)
KMESH = (3, 3, 1)                    # Gamma-centred, <0.05/A for the 4x4 (~9.84 A) cell
PSD = "$PSEUDO_DIR"                  # substituted on kgy


def namelists(calc, pfx, nat, ntyp, has_li):
    spin = ("    nspin           = 2\n    starting_magnetization(%d) = 0.4\n"
            % ntyp) if has_li else ""   # Li is always the LAST species (highest index)
    return f"""&CONTROL
    calculation     = '{calc}'
    prefix          = '{pfx}'
    outdir          = './tmp'
    pseudo_dir      = '{PSD}'
    tprnfor         = .true.
    forc_conv_thr   = 1.0d-3
    nstep           = 200
    disk_io         = 'low'
/
&SYSTEM
    ibrav           = 0
    nat             = {nat}
    ntyp            = {ntyp}
    ecutwfc         = {ECUTWFC}
    ecutrho         = {ECUTRHO}
    occupations     = 'smearing'
    smearing        = 'mv'
    degauss         = 0.01
{spin}    vdw_corr        = 'grimme-d3'
    dftd3_version   = 4
/
&ELECTRONS
    conv_thr        = 1.0d-6
    mixing_beta     = 0.3
    electron_maxstep = 200
/
&IONS
    ion_dynamics    = 'bfgs'
/
"""


def species_block(elems):
    seen = []
    for e in elems:
        if e not in seen:
            seen.append(e)
    # keep Li last so starting_magnetization(ntyp) targets Li
    if "Li" in seen:
        seen = [e for e in seen if e != "Li"] + ["Li"]
    lines = ["ATOMIC_SPECIES"]
    for e in seen:
        lines.append(f"  {e:2s} {MASS[e]:8.3f}  {PSEUDO[e]}")
    return seen, "\n".join(lines) + "\n"


def parse_qe(path):
    txt = open(path).read().splitlines()
    cell, pos, elems = [], [], []
    mode = None
    for l in txt:
        s = l.split()
        if l.strip().upper().startswith("CELL_PARAMETERS"):
            mode = "cell"; continue
        if l.strip().upper().startswith("ATOMIC_POSITIONS"):
            mode = "pos"; continue
        if l.startswith("#") or not s:
            continue
        if mode == "cell" and len(cell) < 3:
            cell.append(l)
        elif mode == "pos" and re.match(r"^[A-Za-z]", s[0]):
            elems.append(s[0]); pos.append(l)
    return cell, elems, pos


def build(path, outdir):
    name = os.path.splitext(os.path.basename(path))[0]
    cell, elems, pos = parse_qe(path)
    has_li = "Li" in elems
    order, spec = species_block(elems)
    # reorder atoms so species grouping is clean (QE tolerates mixed, but tidy)
    body = ["CELL_PARAMETERS angstrom", *cell, "", spec.rstrip(),
            "", "ATOMIC_POSITIONS angstrom", *pos, "",
            f"K_POINTS automatic\n  {KMESH[0]} {KMESH[1]} {KMESH[2]}  0 0 0"]
    inp = namelists("relax", name[:12], len(pos), len(order), has_li) + "\n".join(body) + "\n"
    open(f"{outdir}/{name}.in", "w").write(inp)
    return name, len(pos), order, has_li


def li_atom(outdir):
    """Isolated Li atom in a 15 A box (E_ads reference), gamma, spin-polarised."""
    box = 15.0
    inp = namelists("scf", "li_atom", 1, 1, True).replace(
        "starting_magnetization(1) = 0.4", "starting_magnetization(1) = 1.0")
    inp += f"""CELL_PARAMETERS angstrom
  {box:.4f} 0.0 0.0
  0.0 {box:.4f} 0.0
  0.0 0.0 {box:.4f}

ATOMIC_SPECIES
  Li {MASS['Li']:8.3f}  {PSEUDO['Li']}

ATOMIC_POSITIONS angstrom
  Li  {box/2:.4f} {box/2:.4f} {box/2:.4f}

K_POINTS gamma
"""
    open(f"{outdir}/Li_atom.in", "w").write(inp)


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = f"{here}/periodic"
    out = f"{here}/qe_inputs"
    os.makedirs(out, exist_ok=True)
    print("QE inputs (PBE-D3BJ, PAW, ecutwfc %.0f Ry, k %dx%dx%d, mv smear) [Shi-matched]:"
          % (ECUTWFC, *KMESH))
    for f in sorted(glob.glob(f"{src}/*.qe")):
        name, nat, order, li = build(f, out)
        print(f"  {name:16s} nat={nat:3d} species={order} {'(nspin2)' if li else ''}")
    li_atom(out)
    print("  Li_atom          nat=  1 species=['Li'] (nspin2, gamma, 15A box)")
    print(f"-> {out}/  ($PSEUDO_DIR substituted on kgy).")
    print("E_ads(X) = E(Li_on_X) - E(X) - E(Li_atom); sandwich test: E_ads(gallery) < both singles?")


if __name__ == "__main__":
    main()
