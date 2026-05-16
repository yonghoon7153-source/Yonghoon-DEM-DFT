#!/usr/bin/env python
"""generate_dft_inputs.py — generate QE pw.in files for Top-N MLIP winners.

UMA-s-1p1 is a general MLIP that has known bias for sulfide systems
(Wang 2025 npj Comp Mater reports PES softening / Li diffusivity over-
estimation). For paper-grade B0 / band gap / Bader / PDOS we need DFT
spot-checks on the top MLIP candidates.

This tool reads the final FINAL_RANKING.json (from combine_rankings.py)
and generates QE input files for the top N structures, using the same
template as our Nd-EOS pipeline (52-atom cell, ecutwfc=52 Ry, K=2×2×1).

Each top winner gets its own directory with:
  relax.in        — QE relax input (cell+positions, BFGS)
  pseudo_list.txt — required pseudopotentials for this structure

Then user scp's the directory to KISTI and runs sbatch.

Usage:
  python3 tools/doping/generate_dft_inputs.py \\
      --ranking runs/tier_.../FINAL_RANKING.json \\
      --top 10 \\
      --out runs/tier_.../dft_inputs/
"""
import argparse
import json
import shutil
import sys
from pathlib import Path

from ase.io import read

sys.path.insert(0, str(Path(__file__).parent))
from _provenance import get_provenance


PSEUDO_DIR_KISTI = '/scratch/x3430a02/kgy/manuscript_support/pseudo'

# Element → mass + pseudopotential filename (matches Nd-EOS prepare script)
PSEUDOS = {
    'Li': ('6.9410',   'li_pbe_v1_4_uspp_F.UPF'),
    'P':  ('30.9740',  'P_pbe-n-rrkjus_psl_1_0_0.UPF'),
    'S':  ('32.0650',  's_pbe_v1_4_uspp_F.UPF'),
    'Cl': ('35.4530',  'cl_pbe_v1_4_uspp_F.UPF'),
    'Br': ('79.9040',  'br_pbe_v1.4.uspp.F.UPF'),
    'I':  ('126.9045', 'I.pbe-n-rrkjus_psl.0.2.UPF'),
    'F':  ('18.9984',  'F.pbe-n-kjpaw_psl.0.1.UPF'),
    'O':  ('15.9994',  'O.pbe-n-kjpaw_psl.0.1.UPF'),
    'N':  ('14.0067',  'N.pbe-n-rrkjus_psl.0.1.UPF'),
    # Cations
    'Nd': ('144.242',  'Nd.paw.z_14.atompaw.wentzcovitch.v1.2.upf'),
    'La': ('138.9055', 'La.paw.z_11.atompaw.wentzcovitch.v1.2.upf'),
    'Sm': ('150.36',   'Sm.paw.z_14.atompaw.wentzcovitch.v1.2.upf'),
    'Y':  ('88.9059',  'Y.pbe-spn-kjpaw_psl.1.0.0.UPF'),
    'Sc': ('44.9559',  'Sc.pbe-spn-kjpaw_psl.0.2.3.UPF'),
    'Al': ('26.9815',  'Al.pbe-n-kjpaw_psl.1.0.0.UPF'),
    'Mg': ('24.3050',  'Mg.pbe-n-kjpaw_psl.0.3.0.UPF'),
    'Zn': ('65.38',    'Zn.pbe-dnl-kjpaw_psl.1.0.0.UPF'),
    'Ca': ('40.0780',  'Ca.pbe-spn-kjpaw_psl.1.0.0.UPF'),
    'Sr': ('87.62',    'Sr.pbe-spn-kjpaw_psl.1.0.0.UPF'),
    'Ba': ('137.327',  'Ba.pbe-spn-kjpaw_psl.1.0.0.UPF'),
    'Cu': ('63.546',   'Cu.pbe-dn-kjpaw_psl.1.0.0.UPF'),
    'Ag': ('107.868',  'Ag.pbe-n-kjpaw_psl.1.0.0.UPF'),
    'Ti': ('47.867',   'Ti.pbe-spn-kjpaw_psl.1.0.0.UPF'),
    'Zr': ('91.224',   'Zr.pbe-spn-kjpaw_psl.1.0.0.UPF'),
    'Hf': ('178.49',   'Hf.pbe-spn-kjpaw_psl.1.0.0.UPF'),
    'Si': ('28.0855',  'Si.pbe-n-kjpaw_psl.1.0.0.UPF'),
    'Ge': ('72.63',    'Ge.pbe-dn-kjpaw_psl.1.0.0.UPF'),
    'Sn': ('118.710',  'Sn.pbe-dn-kjpaw_psl.1.0.0.UPF'),
    'Sb': ('121.76',   'Sb.pbe-n-kjpaw_psl.1.0.0.UPF'),
    'Bi': ('208.98',   'Bi.pbe-dn-kjpaw_psl.1.0.0.UPF'),
    'B':  ('10.811',   'B.pbe-n-kjpaw_psl.1.0.0.UPF'),
    'V':  ('50.9415',  'V.pbe-spnl-kjpaw_psl.1.0.0.UPF'),
    'Nb': ('92.9064',  'Nb.pbe-spn-kjpaw_psl.1.0.0.UPF'),
    'Ta': ('180.9479', 'Ta.pbe-spn-kjpaw_psl.1.0.0.UPF'),
    'W':  ('183.84',   'W.pbe-spn-kjpaw_psl.1.0.0.UPF'),
    'Mo': ('95.95',    'Mo.pbe-spn-kjpaw_psl.1.0.0.UPF'),
    'Cr': ('51.9961',  'Cr.pbe-spn-kjpaw_psl.1.0.0.UPF'),
    'Mn': ('54.9380',  'Mn.pbe-spn-kjpaw_psl.0.3.1.UPF'),
    'Fe': ('55.845',   'Fe.pbe-spn-kjpaw_psl.0.2.1.UPF'),
    'Co': ('58.9332',  'Co.pbe-spn-kjpaw_psl.0.3.1.UPF'),
    'Ni': ('58.6934',  'Ni.pbe-spn-kjpaw_psl.1.0.0.UPF'),
}


def generate_pwin(atoms, prefix: str, ecutwfc=52, ecutrho=520,
                 kpoints='2 2 1') -> str:
    species = sorted(set(atoms.get_chemical_symbols()))
    ntyp = len(species)
    nat = len(atoms)
    cell = atoms.cell.array
    frac = atoms.get_scaled_positions()
    syms = atoms.get_chemical_symbols()

    missing = [s for s in species if s not in PSEUDOS]
    if missing:
        raise ValueError(f"Missing pseudopotentials for {missing}; add to PSEUDOS")

    lines = []
    lines.append("&CONTROL")
    lines.append("    calculation = 'relax'")
    lines.append(f"    prefix      = '{prefix}'")
    lines.append("    outdir      = './tmp'")
    lines.append(f"    pseudo_dir  = '{PSEUDO_DIR_KISTI}'")
    lines.append("    tprnfor     = .true.")
    lines.append("    tstress     = .true.")
    lines.append("    etot_conv_thr = 1.0d-6")
    lines.append("    forc_conv_thr = 1.0d-4")
    lines.append("    nstep        = 200")
    lines.append("/")
    lines.append("&SYSTEM")
    lines.append("    ibrav       = 0")
    lines.append(f"    nat         = {nat}")
    lines.append(f"    ntyp        = {ntyp}")
    lines.append(f"    ecutwfc     = {ecutwfc}")
    lines.append(f"    ecutrho     = {ecutrho}")
    lines.append("    occupations = 'smearing'")
    lines.append("    smearing    = 'mv'")
    lines.append("    degauss     = 0.01")
    lines.append("    nosym       = .true.")
    lines.append("/")
    lines.append("&ELECTRONS")
    lines.append("    conv_thr     = 1.0d-8")
    lines.append("    mixing_beta  = 0.2")
    lines.append("    diagonalization = 'david'")
    lines.append("/")
    lines.append("&IONS")
    lines.append("    ion_dynamics = 'bfgs'")
    lines.append("/")
    lines.append("&CELL")
    lines.append("    cell_dynamics = 'bfgs'")
    lines.append("    press_conv_thr = 0.5")
    lines.append("/")
    lines.append("ATOMIC_SPECIES")
    for s in species:
        mass, ppf = PSEUDOS[s]
        lines.append(f"  {s}  {mass}  {ppf}")
    lines.append("CELL_PARAMETERS angstrom")
    for row in cell:
        lines.append(f"  {row[0]:14.10f}  {row[1]:14.10f}  {row[2]:14.10f}")
    lines.append("ATOMIC_POSITIONS crystal")
    for sym, fr in zip(syms, frac):
        lines.append(f"  {sym}  {fr[0]:14.10f}  {fr[1]:14.10f}  {fr[2]:14.10f}")
    lines.append("K_POINTS automatic")
    lines.append(f"  {kpoints} 0 0 0")
    return "\n".join(lines) + "\n"


def main():
    p = argparse.ArgumentParser(description=__doc__,
                               formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('--ranking', required=True,
                  help='FINAL_RANKING.json from combine_rankings.py')
    p.add_argument('--top', type=int, default=10)
    p.add_argument('--out', required=True)
    p.add_argument('--ecutwfc', type=float, default=52)
    p.add_argument('--ecutrho', type=float, default=520)
    p.add_argument('--kpoints', default='2 2 1')
    args = p.parse_args()

    data = json.loads(Path(args.ranking).read_text())
    rows = data.get('rows', [])[:args.top]
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    # Resume: skip if relax.in already exists
    summary = {'provenance': get_provenance(), 'generated': [], 'skipped': [],
               'failed': []}
    for i, row in enumerate(rows, 1):
        name = row.get('name', f'top{i}')
        work = out / f'rank{i:02d}_{name}'
        relax_in = work / 'relax.in'
        if relax_in.exists():
            summary['skipped'].append(name)
            print(f"  [skip] {name} (relax.in exists)")
            continue
        # We need the xyz to read coordinates — look up from screening
        xyz_candidates = [
            row.get('xyz_input'), row.get('xyz_file'),
            row.get('_anneal', {}).get('post_relax_xyz'),
        ]
        xyz_path = next((Path(x) for x in xyz_candidates
                        if x and Path(x).exists()), None)
        if xyz_path is None:
            summary['failed'].append({'name': name, 'reason': 'no xyz found'})
            print(f"  ⚠ {name}: no xyz available")
            continue
        try:
            atoms = read(str(xyz_path))
            work.mkdir(parents=True, exist_ok=True)
            relax_in.write_text(generate_pwin(atoms, name,
                                              args.ecutwfc, args.ecutrho,
                                              args.kpoints))
            # Copy xyz for traceability
            shutil.copy(str(xyz_path), str(work / 'init.xyz'))
            # List required pseudos
            species = sorted(set(atoms.get_chemical_symbols()))
            (work / 'pseudo_list.txt').write_text(
                '\n'.join(PSEUDOS[s][1] for s in species) + '\n')
            summary['generated'].append({
                'name': name, 'path': str(work),
                'rank': i,
                'composite_score': row.get('score_combined'),
                'B0_GPa_MLIP': row.get('B0_GPa'),
                'E_young_GPa_MLIP': row.get('E_young_GPa'),
            })
            print(f"  ✓ rank{i:02d}_{name} → {work}")
        except Exception as e:
            summary['failed'].append({'name': name, 'reason': str(e)})
            print(f"  ✗ {name}: {e}")

    (out / 'dft_input_summary.json').write_text(
        json.dumps(summary, indent=2, default=str))
    print(f"\n✓ Generated {len(summary['generated'])} DFT inputs "
          f"({len(summary['skipped'])} skipped, "
          f"{len(summary['failed'])} failed)")
    print(f"\nNext: scp -r {out} <KISTI>:/path/  then sbatch <run script>")


if __name__ == '__main__':
    main()
