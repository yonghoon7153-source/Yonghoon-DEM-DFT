#!/usr/bin/env python
"""prepare_dft_eos_nd.py — Generate DFT EOS pw.in files for Nd-doped LPSCl.

Takes UMA-relaxed structures for top-2 pairs and generates:
  pair_XX_eos/v094/relax.in
  pair_XX_eos/v096/relax.in
  ...
  pair_XX_eos/v106/relax.in

Template based on comp5_lpscbr (most recent, May 13).
Adds Nd PP. Uses V0_BM from UMA EOS results to set cell scale per volume.

Usage:
  python3 prepare_dft_eos_nd.py \\
      --eos_results /scratch/x3430a02/kgy/nd_doped_modelc/2_uma_eos_predft/results/eos_results.json \\
      --out_base /scratch/x3430a02/kgy/nd_doped_modelc/3_dft_eos
"""
import argparse
import json
import shutil
from pathlib import Path
import numpy as np
from ase.io import read


# Template constants (from comp5_lpscbr/dft_eos/v100/relax.in)
PSEUDO_DIR = '/scratch/x3430a02/kgy/manuscript_support/pseudo'
ECUTWFC = 52.0
ECUTRHO = 520.0
DEGAUSS = 0.01
KPOINTS = "2 2 1 0 0 0"

# Pseudopotentials (PBE, USPP/PAW)
PSEUDOS = {
    'Li': ('6.9410',  'li_pbe_v1_4_uspp_F.UPF'),
    'P':  ('30.9740', 'P_pbe-n-rrkjus_psl_1_0_0.UPF'),
    'S':  ('32.0650', 's_pbe_v1_4_uspp_F.UPF'),
    'Br': ('79.9040', 'br_pbe_v1.4.uspp.F.UPF'),
    'Cl': ('35.4530', 'cl_pbe_v1_4_uspp_F.UPF'),
    'Nd': ('144.242', 'Nd.paw.z_14.atompaw.wentzcovitch.v1.2.upf'),
    # 2026-05-16 fix: Nd2O3-doped LPSCl needs O. SSSP_1.3.0 efficiency
    # PAW available at /scratch/x3430a02/kgy/pseudo/.
    'O':  ('15.9994', 'O.pbe-n-kjpaw_psl.0.1.UPF'),
}
ND_PP_SRC = '/scratch/x3430a02/kgy/pseudo/Nd.paw.z_14.atompaw.wentzcovitch.v1.2.upf'
O_PP_SRC  = '/scratch/x3430a02/kgy/pseudo/O.pbe-n-kjpaw_psl.0.1.UPF'

# Volume ratios for DFT EOS (matches comp5 pattern)
VOLUME_RATIOS = [0.94, 0.96, 0.98, 1.00, 1.02, 1.04, 1.06]


def generate_pwin(atoms, prefix: str, cell_scale: float) -> str:
    """Generate pw.in content from atoms + cell scale factor."""
    species = sorted(set(atoms.get_chemical_symbols()))
    ntyp = len(species)
    nat = len(atoms)

    # Cell (scaled)
    cell = atoms.cell.array * cell_scale

    # Positions in crystal coords (cell-invariant under scaling)
    frac = atoms.get_scaled_positions()
    symbols = atoms.get_chemical_symbols()

    lines = []
    lines.append("&CONTROL")
    lines.append("    calculation = 'relax'")
    lines.append(f"    prefix      = '{prefix}'")
    lines.append("    outdir      = './tmp'")
    lines.append(f"    pseudo_dir  = '{PSEUDO_DIR}'")
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
    lines.append(f"    ecutwfc     = {ECUTWFC}")
    lines.append(f"    ecutrho     = {ECUTRHO}")
    lines.append("    occupations = 'smearing'")
    lines.append("    smearing    = 'mv'")
    lines.append(f"    degauss     = {DEGAUSS}")
    lines.append("    nosym       = .true.")
    lines.append("/")
    lines.append("&ELECTRONS")
    # Charge-sloshing-tolerant settings for Nd-doped LPSCl (Nd f-electron
    # near-degeneracy at V_ref causes oscillation under plain mixing).
    # Empirically derived 2026-05-17 from pair01 SCF fail diagnosis:
    # plain mixing with beta=0.1 oscillates between 10^-3 and 10^-4
    # forever. local-TF screening + CG diagonalization + beta=0.05
    # breaks the oscillation. Cost: ~1.5x slower per SCF on close-pair
    # (pair02) compared to plain Davidson, but enables reference-pair
    # (pair01) convergence which is otherwise impossible.
    lines.append("    conv_thr    = 1.0d-6")
    lines.append("    mixing_beta = 0.05")
    lines.append("    mixing_mode = 'local-TF'")
    lines.append("    electron_maxstep = 500")
    lines.append("    diagonalization = 'cg'")
    lines.append("/")
    lines.append("&IONS")
    lines.append("    ion_dynamics = 'bfgs'")
    lines.append("/")
    lines.append("&CELL")
    lines.append("    cell_dofree = 'none'")
    lines.append("/")
    lines.append("")
    lines.append("ATOMIC_SPECIES")
    for sp in species:
        if sp not in PSEUDOS:
            raise ValueError(f"Element {sp} not in PSEUDOS database. Add manually.")
        mass, ppf = PSEUDOS[sp]
        lines.append(f"  {sp:<4} {mass:>10}  {ppf}")
    lines.append("")
    lines.append("CELL_PARAMETERS angstrom")
    for i in range(3):
        lines.append(f"  {cell[i,0]:16.10f}  {cell[i,1]:16.10f}  {cell[i,2]:16.10f}")
    lines.append("")
    lines.append("ATOMIC_POSITIONS crystal")
    for sp, p in zip(symbols, frac):
        lines.append(f"  {sp:<4} {p[0]:16.10f}  {p[1]:16.10f}  {p[2]:16.10f}")
    lines.append("")
    lines.append("K_POINTS automatic")
    lines.append(f"  {KPOINTS}")
    return "\n".join(lines) + "\n"


def process_pair(pair_name: str, rank: int, relaxed_cif: Path, out_base: Path) -> dict:
    print(f"\n{'='*70}")
    print(f"Rank {rank}: {pair_name}")
    print(f"  Reading: {relaxed_cif}")
    atoms = read(relaxed_cif)
    species = sorted(set(atoms.get_chemical_symbols()))
    print(f"  Atoms: {len(atoms)}, species: {species}")
    print(f"  V_ref: {atoms.get_volume():.3f} Å³")

    pair_dir = out_base / f'pair{rank:02d}_{pair_name}'
    pair_dir.mkdir(parents=True, exist_ok=True)

    generated = []
    for r in VOLUME_RATIOS:
        vlabel = f"v{int(100*r):03d}"
        v_dir = pair_dir / vlabel
        v_dir.mkdir(exist_ok=True)
        scale = r ** (1/3)
        prefix = f"nd_pair{rank:02d}_{vlabel}"
        pwin = generate_pwin(atoms, prefix, scale)
        (v_dir / 'relax.in').write_text(pwin)
        # Initial volume check
        cell_new = atoms.cell.array * scale
        from numpy.linalg import det
        V_new = abs(det(cell_new))
        generated.append({'vlabel': vlabel, 'ratio': r, 'scale': scale, 'V': float(V_new)})
        print(f"  {vlabel}: scale={scale:.5f}, V={V_new:.2f} Å³  → {v_dir}/relax.in")

    return {'pair': pair_name, 'rank': rank, 'pair_dir': str(pair_dir),
            'volumes': generated, 'n_atoms': len(atoms),
            'species': species}


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--eos_results', required=True, help='UMA eos_results.json')
    parser.add_argument('--relaxed_dir', help='Directory with relaxed cifs '
                       '(default: same dir as eos_results)')
    parser.add_argument('--out_base', required=True, help='Output base dir')
    args = parser.parse_args()

    eos_data = json.load(open(args.eos_results))
    out_base = Path(args.out_base)
    out_base.mkdir(parents=True, exist_ok=True)

    if args.relaxed_dir:
        rel_dir = Path(args.relaxed_dir)
    else:
        rel_dir = Path(args.eos_results).parent / 'relaxed_structures'

    print("=" * 70)
    print("Prepare DFT EOS for Nd-doped LPSCl (top-2 from UMA screening)")
    print("=" * 70)
    print(f"  Relaxed cifs from: {rel_dir}")
    print(f"  Output base:       {out_base}")
    print(f"  Template:          comp5_lpscbr (May 13, ecutwfc=52, ecutrho=520)")

    # Copy Nd + O PPs to pseudo_dir if not already there
    for src in (ND_PP_SRC, O_PP_SRC):
        dst = Path(PSEUDO_DIR) / Path(src).name
        label = Path(src).stem.split('.')[0]
        if not dst.exists():
            print(f"\n  Copying {label} PP: {src} → {dst}")
            try:
                shutil.copy(src, dst)
            except PermissionError:
                print(f"  ⚠️  Cannot write to {PSEUDO_DIR}. Run manually:")
                print(f"     cp {src} {dst}")
        else:
            print(f"\n  {label} PP already present: {dst}")

    summary = {}
    for pair_name, info in eos_data.items():
        rank = info['rank']
        cif = rel_dir / f'{pair_name}_relaxed.cif'
        if not cif.exists():
            print(f"\n  ⚠️  Missing {cif} — skip {pair_name}")
            continue
        summary[pair_name] = process_pair(pair_name, rank, cif, out_base)

    # Save summary
    json.dump(summary, open(out_base / 'dft_eos_prep_summary.json', 'w'),
              indent=2, default=str)
    print(f"\n{'='*70}")
    print(f"✓ Generated pw.in files for {len(summary)} pairs × {len(VOLUME_RATIOS)} volumes")
    print(f"  Output: {out_base}/pair??_*/{{v094..v106}}/relax.in")
    print(f"  Summary: {out_base}/dft_eos_prep_summary.json")
    print(f"\nNext: Submit DFT EOS with sbatch_dft_eos_rank{{1,2}}.sh")


if __name__ == '__main__':
    main()
