#!/usr/bin/env python
"""run_uma_screening.py — UMA MLIP relaxation + Tier-1 descriptors.

Reads structures_summary.json from substitute_struct.py and runs UMA full
relaxation (cell + positions, FrechetCellFilter) on each candidate. Computes
volume change, energy per atom, substitution energy, lattice parameters.

Auto-resumes: skips structures already in uma_screening_results.json.

Usage:
  python3 run_uma_screening.py \\
      --summary data/doping_screening/structures/structures_summary.json \\
      --baseline data/lpscl_bulk_uma_relaxed.json \\
      --out data/doping_screening/uma_screening_results.json \\
      --device cuda --task omat

  # Without baseline (computes on-the-fly from base CIF)
  python3 run_uma_screening.py \\
      --summary data/doping_screening/structures/structures_summary.json \\
      --base data/lpscl_bulk.cif \\
      --out data/doping_screening/uma_screening_results.json
"""
import argparse
import json
import time
from pathlib import Path
import numpy as np
from ase.io import read
from ase.optimize import FIRE

try:
    from ase.filters import FrechetCellFilter as CellFilter
except ImportError:
    try:
        from ase.constraints import ExpCellFilter as CellFilter
    except ImportError:
        from ase.constraints import UnitCellFilter as CellFilter


def load_uma_calc(device: str = 'cuda', task: str = 'omat'):
    """Load UMA-s-1p1 calculator (FAIRChem)."""
    from fairchem.core import pretrained_mlip, FAIRChemCalculator
    predictor = pretrained_mlip.get_predict_unit('uma-s-1p1', device=device)
    return FAIRChemCalculator(predictor, task_name=task)


def relax_structure(atoms, calc, fmax: float = 0.05, steps: int = 300,
                    cell_relax: bool = True):
    """Full relaxation: cell + positions if cell_relax else positions only."""
    atoms.calc = calc
    if cell_relax:
        target = CellFilter(atoms)
    else:
        target = atoms
    opt = FIRE(target, logfile=None)
    opt.run(fmax=fmax, steps=steps)
    converged = opt.get_number_of_steps() < steps
    return atoms, converged, opt.get_number_of_steps()


def compute_descriptors(atoms, baseline_e_per_atom: float,
                        chem_potentials: dict = None) -> dict:
    """Tier-1 descriptors after relaxation."""
    e_total = float(atoms.get_potential_energy())
    n = len(atoms)
    e_per_atom = e_total / n
    cell = atoms.get_cell()
    a, b, c = cell.lengths()
    alpha, beta, gamma = cell.angles()
    vol = float(atoms.get_volume())
    syms = atoms.get_chemical_symbols()
    composition = {el: int(c) for el, c in zip(*np.unique(syms, return_counts=True))}
    return {
        'e_total': e_total,
        'e_per_atom': e_per_atom,
        'de_per_atom_vs_baseline': e_per_atom - baseline_e_per_atom,
        'volume': vol,
        'volume_per_atom': vol / n,
        'lattice_a': float(a),
        'lattice_b': float(b),
        'lattice_c': float(c),
        'lattice_alpha': float(alpha),
        'lattice_beta': float(beta),
        'lattice_gamma': float(gamma),
        'n_atoms': n,
        'composition': composition,
    }


def get_baseline(args, calc) -> dict:
    """Get or compute clean LPSCl baseline (e_per_atom, volume_per_atom)."""
    if args.baseline and Path(args.baseline).exists():
        return json.loads(Path(args.baseline).read_text())
    if not args.base:
        raise ValueError("Provide --baseline (cached) or --base (CIF) for baseline")
    print(f"Computing LPSCl baseline from: {args.base}")
    base = read(args.base)
    base, conv, nsteps = relax_structure(base, calc,
                                         fmax=args.fmax, steps=args.steps,
                                         cell_relax=True)
    bl = {
        'e_total': float(base.get_potential_energy()),
        'e_per_atom': float(base.get_potential_energy()) / len(base),
        'volume': float(base.get_volume()),
        'volume_per_atom': float(base.get_volume()) / len(base),
        'n_atoms': len(base),
        'converged': conv,
        'n_steps': nsteps,
    }
    if args.baseline:
        Path(args.baseline).write_text(json.dumps(bl, indent=2))
        print(f"  baseline cached → {args.baseline}")
    print(f"  baseline E/atom = {bl['e_per_atom']:.4f} eV, V0 = {bl['volume']:.2f} Å³")
    return bl


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                    formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--summary', required=True,
                       help='structures_summary.json from substitute_struct.py')
    parser.add_argument('--baseline',
                       help='Cached baseline JSON (LPSCl undoped relaxed)')
    parser.add_argument('--base',
                       help='LPSCl base CIF (used if baseline not cached)')
    parser.add_argument('--out', required=True,
                       help='Output uma_screening_results.json')
    parser.add_argument('--device', default='cuda',
                       help="UMA device: 'cuda' or 'cpu'")
    parser.add_argument('--task', default='omat',
                       help="UMA task_name (default: omat)")
    parser.add_argument('--fmax', type=float, default=0.05,
                       help='Force convergence (eV/Å)')
    parser.add_argument('--steps', type=int, default=300,
                       help='Max FIRE steps')
    parser.add_argument('--no_cell_relax', action='store_true',
                       help='Position-only relaxation (fix cell)')
    parser.add_argument('--limit', type=int, default=None,
                       help='Limit to first N structures (debug)')
    args = parser.parse_args()

    summary = json.loads(Path(args.summary).read_text())
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    # Load existing (resume support)
    done = {}
    if out_path.exists():
        existing = json.loads(out_path.read_text())
        done = {r['name']: r for r in existing.get('results', [])}
        print(f"Resume: {len(done)} structures already done")

    print(f"Loading UMA-s-1p1 ({args.device}, task={args.task})...")
    calc = load_uma_calc(args.device, args.task)

    baseline = get_baseline(args, calc)

    todo = [s for s in summary if s['name'] not in done]
    if args.limit:
        todo = todo[:args.limit]
    print(f"To process: {len(todo)}/{len(summary)} structures")

    results = list(done.values())
    failed = []
    t_start = time.time()

    for i, struct_meta in enumerate(todo):
        name = struct_meta['name']
        xyz = struct_meta['xyz_file']
        print(f"\n[{i+1}/{len(todo)}] {name}")
        try:
            atoms = read(xyz)
            t0 = time.time()
            atoms, conv, nsteps = relax_structure(
                atoms, calc, fmax=args.fmax, steps=args.steps,
                cell_relax=not args.no_cell_relax)
            dt = time.time() - t0
            desc = compute_descriptors(atoms, baseline['e_per_atom'])
            dV = (desc['volume'] - baseline['volume'] *
                  (desc['n_atoms'] / baseline['n_atoms'])) / (
                  baseline['volume'] * desc['n_atoms'] / baseline['n_atoms'])
            rec = {
                **struct_meta,
                'uma_relaxed': desc,
                'baseline_e_per_atom': baseline['e_per_atom'],
                'baseline_volume_per_atom': baseline['volume_per_atom'],
                'dV_over_V0': dV,
                'converged': conv,
                'n_relax_steps': nsteps,
                'relax_time_s': dt,
            }
            results.append(rec)
            print(f"  ✓ E/atom={desc['e_per_atom']:.4f} eV, "
                  f"ΔV/V0={dV*100:+.2f}%, "
                  f"steps={nsteps}, t={dt:.1f}s, conv={conv}")
        except Exception as e:
            failed.append({'name': name, 'error': str(e)})
            print(f"  ❌ FAILED: {e}")

        # Periodic save
        if (i + 1) % 5 == 0 or (i + 1) == len(todo):
            out_path.write_text(json.dumps({
                'baseline': baseline,
                'n_done': len(results),
                'n_failed': len(failed),
                'failed': failed,
                'results': results,
            }, indent=2, default=str))

    t_total = time.time() - t_start
    print(f"\n{'='*60}")
    print(f"✓ UMA screening done: {len(results)} structures, "
          f"{len(failed)} failed, {t_total:.1f}s")
    print(f"✓ Results: {out_path}")


if __name__ == '__main__':
    main()
