#!/usr/bin/env python3
"""phaseB_v7c_dft_binding.py — SDCP v7c | Phase-B DFT+U cross-check of the
LiNiO2(104) binding energy on the Phase-A (UMA) geometries.

Phase-A (UMA) gave doped_sulfonate_down_r0 = -0.935 vs neutral -0.893 eV
(Delta 0.04) — too close to trust, because UMA has no charge/spin knob and
sees only the radical *geometry*. Phase-B re-scores the SAME geometries with
DFT+U (the arbiter). We emit 5 single-point SCF inputs:

  slab            E_slab  (the shared reference)
  complex_doped   E(slab + doped radical, champion orientation)
  complex_neutral E(slab + neutral molecule, same orientation)
  mol_doped       E_mol(doped)   gas ref, doublet
  mol_neutral     E_mol(neutral) gas ref, singlet

  E_bind(tag) = E(complex_tag) - E_slab - E_mol(tag)     [negative = binding]
  Verdict = sign & size of  E_bind(doped) - E_bind(neutral).

Settings are cloned VERBATIM from reference_dft_v2/scf_u62.in — the converged
LiNiO2(104) recipe — with ONE deliberate change (u62c plan): the FSM line
`tot_magnetization = 0.0` is DROPPED for the slab/complexes so the adsorbed
radical's spin is free to find its own ground state; only the Ni AFM guess
(starting_magnetization +/-0.3) is kept. The Ni1/Ni2 sublattice split is
inherited from scf_u62.in by nearest-position matching (both are the same
96-atom (104) slab; relaxation drift << Ni-Ni spacing, so the map is 1:1).

Single-point (calculation='scf'): the cross-check isolates the electronic/U
effect at fixed UMA geometry — apples-to-apples with Phase-A.

Usage (on KISTI, where scf_u62.in + phaseA xyz live):
  conda activate uma   # only for ASE io; no GPU needed
  python3 phaseB_v7c_dft_binding.py \
      --ref_scf     /data/work/runs/sdcp_linio2_binding/reference_dft_v2/scf_u62.in \
      --slab        /data/work/runs/sdcp_linio2_binding/reference/slab_relaxed.xyz \
      --complex_doped   /data/work/runs/sdcp_linio2_binding/phaseA_v7c/complex_doped_sulfonate_down_r0.xyz \
      --complex_neutral /data/work/runs/sdcp_linio2_binding/phaseA_v7c/complex_neutral_sulfonate_down_r0.xyz \
      --mol_doped   /data/work/runs/sdcp_linio2_binding/inputs/sdcp_v7c/sdcp_v7c_doped.xyz \
      --mol_neutral /data/work/runs/sdcp_linio2_binding/inputs/sdcp_v7c/sdcp_v7c_neutral.xyz \
      --pseudo_dir  /data/work/pseudo \
      --out         /data/work/runs/sdcp_linio2_binding/phaseB_v7c
Writes <out>/{slab,complex_doped,complex_neutral,mol_doped,mol_neutral}/scf.in
plus <out>/README_harvest.txt (E_bind formula + a grep-the-energies snippet).
"""
import argparse
import os
import re
import numpy as np
from ase.io import read

# ---- cloned from scf_u62.in (reference_dft_v2) ------------------------------
ECUTWFC = 60.0
ECUTRHO = 480.0
DEGAUSS = 0.03            # smearing = 'mv'
CONV_THR = 1.0e-6
MIX_BETA = 0.03          # local-TF, ndim 20 — the slow/safe recipe that converged
MIX_NDIM = 20
U_NI = 6.2               # HUBBARD ortho-atomic, Ni1-3d / Ni2-3d
AFM_MAG = 0.3            # starting_magnetization Ni1 +0.3 / Ni2 -0.3
KPTS_SLAB = "2 2 1 0 0 0"
MOL_VACUUM = 12.0        # A vacuum around gas-phase molecule box

# PBE USPP/PAW pseudos (all confirmed present in /data/work/pseudo)
PSEUDOS = {
    'Li':  ('6.940',   'li_pbe_v1.4.uspp.F.UPF'),
    'Ni1': ('58.690',  'ni_pbe_v1.4.uspp.F.UPF'),
    'Ni2': ('58.690',  'ni_pbe_v1.4.uspp.F.UPF'),
    'O':   ('15.999',  'O.pbe-n-kjpaw_psl.0.1.UPF'),
    'C':   ('12.011',  'C.pbe-n-kjpaw_psl.1.0.0.UPF'),
    'H':   ('1.008',   'H.pbe-rrkjus_psl.1.0.0.UPF'),
    'S':   ('32.065',  's_pbe_v1.4.uspp.F.UPF'),
}
SPECIES_ORDER = ['Li', 'Ni1', 'Ni2', 'O', 'C', 'H', 'S']


def parse_ref_ni(ref_scf):
    """Extract Ni1/Ni2 cartesian positions from a QE input (the AFM partition)."""
    with open(ref_scf) as f:
        lines = f.readlines()
    # cell
    cell = None
    for i, ln in enumerate(lines):
        if ln.strip().upper().startswith('CELL_PARAMETERS'):
            cell = np.array([[float(x) for x in lines[i + k].split()[:3]]
                             for k in (1, 2, 3)])
            break
    # atomic positions
    for i, ln in enumerate(lines):
        u = ln.strip().upper()
        if u.startswith('ATOMIC_POSITIONS'):
            crystal = 'CRYSTAL' in u
            j = i + 1
            ni1, ni2 = [], []
            while j < len(lines):
                s = lines[j].split()
                if len(s) < 4 or not re.match(r'^[A-Za-z]', s[0]):
                    break
                sp = s[0]
                p = np.array([float(s[1]), float(s[2]), float(s[3])])
                if crystal:
                    if cell is None:
                        raise SystemExit("CRYSTAL positions but no CELL_PARAMETERS")
                    p = p @ cell
                if sp == 'Ni1':
                    ni1.append(p)
                elif sp == 'Ni2':
                    ni2.append(p)
                j += 1
            if not ni1 or not ni2:
                raise SystemExit("ref_scf has no Ni1/Ni2 labels — cannot inherit AFM split")
            return np.array(ni1), np.array(ni2), cell
    raise SystemExit("no ATOMIC_POSITIONS in ref_scf")


def split_ni(atoms, ni1_ref, ni2_ref, cell):
    """Return per-atom species labels; each Ni -> Ni1/Ni2 by nearest ref (MIC)."""
    labels = list(atoms.get_chemical_symbols())
    inv = np.linalg.inv(cell) if cell is not None else None
    worst = 0.0
    for idx, sym in enumerate(labels):
        if sym != 'Ni':
            continue
        p = atoms.positions[idx]

        def mind(refs):
            d = refs - p
            if inv is not None:                       # min-image
                f = d @ inv
                f -= np.round(f)
                d = f @ cell
            return np.sqrt((d ** 2).sum(axis=1)).min()
        d1, d2 = mind(ni1_ref), mind(ni2_ref)
        labels[idx] = 'Ni1' if d1 <= d2 else 'Ni2'
        worst = max(worst, min(d1, d2))
    if worst > 1.0:
        print(f"  !! WARNING: a Ni matched its nearest ref at {worst:.2f} A "
              f"(>1.0) — check slab correspondence")
    return labels


def write_scf(path, atoms, labels, kind, kpts, pseudo_dir, prefix):
    """kind in {'slab','complex','molecule_doped','molecule_neutral'}."""
    has_ni = ('Ni1' in labels) or ('Ni2' in labels)
    doped_mol = (kind == 'molecule_doped')
    present = [sp for sp in SPECIES_ORDER if sp in labels]
    ntyp = len(present)
    nat = len(labels)

    sys_lines = [
        "    ibrav           = 0",
        f"    nat             = {nat}",
        f"    ntyp            = {ntyp}",
        f"    ecutwfc         = {ECUTWFC}",
        f"    ecutrho         = {ECUTRHO}",
        "    occupations     = 'smearing'",
        "    smearing        = 'mv'",
        f"    degauss         = {DEGAUSS}",
        "    nspin           = 2",
        "    nosym           = .true.",
    ]
    # spin setup
    if has_ni:                                   # slab / complex: AFM Ni guess, spin free
        sys_lines.append(f"    starting_magnetization(2) = +{AFM_MAG}   ! Ni1 up")
        sys_lines.append(f"    starting_magnetization(3) = -{AFM_MAG}   ! Ni2 down (AFM)")
        # NOTE: FSM tot_magnetization DROPPED on purpose (u62c) so radical spin is free
    else:                                        # isolated molecule
        if doped_mol:
            sys_lines.append("    tot_magnetization = 1.0   ! [M-H] radical = doublet")
            sys_lines.append("    starting_magnetization(1) = 0.1")
        else:
            sys_lines.append("    tot_magnetization = 0.0   ! neutral molecule = singlet")
            sys_lines.append("    starting_magnetization(1) = 0.0")

    body = []
    body.append("&CONTROL")
    body.append("    calculation     = 'scf'")
    body.append(f"    prefix          = '{prefix}'")
    body.append("    outdir          = './tmp'")
    body.append(f"    pseudo_dir      = '{pseudo_dir}'")
    body.append("    tprnfor         = .true.")
    body.append("    tstress         = .false.")
    body.append("    disk_io         = 'low'")
    body.append("/")
    body.append("&SYSTEM")
    body.extend(sys_lines)
    body.append("/")
    body.append("&ELECTRONS")
    body.append(f"    conv_thr        = {CONV_THR}")
    body.append(f"    mixing_beta     = {MIX_BETA}")
    body.append("    mixing_mode     = 'local-TF'")
    body.append(f"    mixing_ndim     = {MIX_NDIM}")
    body.append("    electron_maxstep = 300")
    body.append("    diagonalization = 'david'")
    body.append("/")
    body.append("")
    body.append("ATOMIC_SPECIES")
    for sp in present:
        mass, pp = PSEUDOS[sp]
        body.append(f"  {sp:<3s} {mass:>8s}  {pp}")
    if has_ni:
        body.append("")
        body.append("HUBBARD ortho-atomic")
        body.append(f"U Ni1-3d {U_NI}")
        body.append(f"U Ni2-3d {U_NI}")
    body.append("")
    cell = atoms.cell.array
    body.append("CELL_PARAMETERS angstrom")
    for v in cell:
        body.append(f"  {v[0]:18.12f} {v[1]:18.12f} {v[2]:18.12f}")
    body.append("")
    body.append("ATOMIC_POSITIONS angstrom")
    for lab, p in zip(labels, atoms.positions):
        body.append(f"  {lab:<3s} {p[0]:18.12f} {p[1]:18.12f} {p[2]:18.12f}")
    body.append("")
    body.append("K_POINTS automatic" if kpts != "gamma" else "K_POINTS gamma")
    if kpts != "gamma":
        body.append(f"  {kpts}")
    body.append("")
    with open(path, "w") as f:
        f.write("\n".join(body))


def box_molecule(atoms):
    m = atoms.copy()
    ext = m.positions.max(axis=0) - m.positions.min(axis=0)
    L = ext + 2 * MOL_VACUUM
    m.set_cell(L)
    m.center()
    m.pbc = True
    return m


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ref_scf", required=True)
    ap.add_argument("--slab", required=True)
    ap.add_argument("--complex_doped", required=True)
    ap.add_argument("--complex_neutral", required=True)
    ap.add_argument("--mol_doped", required=True)
    ap.add_argument("--mol_neutral", required=True)
    ap.add_argument("--pseudo_dir", default="/data/work/pseudo")
    ap.add_argument("--out", required=True)
    ap.add_argument("--kpts", default=KPTS_SLAB, help="slab/complex k-grid")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)

    ni1_ref, ni2_ref, cell = parse_ref_ni(a.ref_scf)
    print(f"ref AFM split: Ni1 x{len(ni1_ref)}  Ni2 x{len(ni2_ref)}", flush=True)

    jobs = [
        ("slab",            a.slab,             "slab",             a.kpts,   "pb_slab"),
        ("complex_doped",   a.complex_doped,    "complex",          a.kpts,   "pb_cxd"),
        ("complex_neutral", a.complex_neutral,  "complex",          a.kpts,   "pb_cxn"),
        ("mol_doped",       a.mol_doped,        "molecule_doped",   "gamma",  "pb_mold"),
        ("mol_neutral",     a.mol_neutral,      "molecule_neutral", "gamma",  "pb_moln"),
    ]
    for name, src, kind, kpts, prefix in jobs:
        atoms = read(src)
        if kind.startswith("molecule"):
            atoms = box_molecule(atoms)
            labels = list(atoms.get_chemical_symbols())
        else:
            labels = split_ni(atoms, ni1_ref, ni2_ref, atoms.cell.array)
        d = os.path.join(a.out, name)
        os.makedirs(d, exist_ok=True)
        write_scf(os.path.join(d, "scf.in"), atoms, labels, kind, kpts,
                  a.pseudo_dir, prefix)
        nni = sum(1 for x in labels if x in ('Ni1', 'Ni2'))
        print(f"  {name:16s} nat={len(labels):3d}  Ni={nni:3d}  k={kpts}  -> {name}/scf.in",
              flush=True)

    with open(os.path.join(a.out, "README_harvest.txt"), "w") as f:
        f.write(
            "Phase-B DFT+U binding cross-check (single-point on UMA geometries)\n"
            "  E_bind(tag) = E(complex_tag) - E_slab - E_mol(tag)\n"
            "  verdict     = E_bind(doped) - E_bind(neutral)   (< 0 => doping strengthens)\n\n"
            "Run order (sequential; slab is the heaviest ~96+ atoms):\n"
            "  for j in slab complex_doped complex_neutral mol_doped mol_neutral; do\n"
            "    cd $j && mpirun -np <N> pw.x -in scf.in > scf.out 2>&1; cd ..\n"
            "  done\n\n"
            "Harvest:\n"
            "  for j in slab complex_doped complex_neutral mol_doped mol_neutral; do\n"
            "    printf '%-16s ' $j; grep '! *total energy' $j/scf.out | tail -1; done\n"
            "  # convert Ry->eV (x13.605693) then apply E_bind formula.\n"
        )
    print(f"\nwrote 5 inputs + README_harvest.txt under {a.out}", flush=True)


if __name__ == "__main__":
    main()
