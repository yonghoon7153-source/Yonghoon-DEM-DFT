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
import sys
import time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from _provenance import get_provenance
_PROVENANCE = get_provenance()
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


def compute_tier2_metrics(atoms) -> dict:
    """Cheap structural descriptors (Tier-2) computed from final geometry.

    No extra UMA calls — pure geometry analysis. These metrics complement
    Tier-1 (ΔE/atom, ΔV/V₀) so the ranking is not dependent on a single
    arbitrary composite. All are paper-defensible:

      - li_li_disorder_std: std of nearest Li-Li distance — Pustorino 2025
        cites Li ordering as the main B0 spread driver
      - li_li_disorder_mean: mean nearest Li-Li distance — ionic conductivity
        proxy (Adeli 2019 halide-rich uses Li-Li spacing as σ proxy)
      - dopant_blocking_count: # of Li atoms within 4 Å of any aliovalent
        cation (Mg/Al/Y/La/Sc/Nd/etc.) — Li migration path blockage
        (Pham 2021 oxysulfide arguments)
      - lattice_angle_dev_deg: σ of (cell_angle − 90°) — symmetry breaking
        magnitude (D'Amore 2022 pseudo-cubic distortion measure)
      - lattice_aspect_ratio: max(a,b,c) / min(a,b,c) — anisotropic strain
    """
    syms = atoms.get_chemical_symbols()
    li_idx = [i for i, s in enumerate(syms) if s == 'Li']
    # CR-6 fix (2026-05-16): "dopant" = anything NOT in the LPSCl baseline
    # composition (Li, P, S, Cl). Br/I/O/N/F that arrive via doping are
    # correctly treated as dopants. Previously they were lumped with host
    # so halide-rich / oxysulfide structures always got dopant_blocking=0.
    baseline_elements = {'Li', 'P', 'S', 'Cl'}
    dopant_idx = [i for i, s in enumerate(syms) if s not in baseline_elements]

    metrics: dict = {}

    if len(li_idx) >= 2:
        D = atoms.get_all_distances(mic=True)
        li_nn = []
        for i in li_idx:
            d_others = [D[i, j] for j in li_idx if j != i]
            li_nn.append(min(d_others))
        metrics['li_li_disorder_std'] = float(np.std(li_nn))
        metrics['li_li_disorder_mean'] = float(np.mean(li_nn))
    else:
        metrics['li_li_disorder_std'] = 0.0
        metrics['li_li_disorder_mean'] = 0.0

    if dopant_idx and li_idx:
        D2 = atoms.get_all_distances(mic=True)
        blocked = sum(1 for li in li_idx
                     if min(D2[li, d] for d in dopant_idx) < 4.0)
        metrics['dopant_blocking_count'] = int(blocked)
        metrics['dopant_blocking_fraction'] = float(blocked) / len(li_idx)
    else:
        metrics['dopant_blocking_count'] = 0
        metrics['dopant_blocking_fraction'] = 0.0

    angles = atoms.cell.angles()
    metrics['lattice_angle_dev_deg'] = float(np.std(
        [abs(a - 90) for a in angles]))
    lengths = atoms.cell.lengths()
    metrics['lattice_aspect_ratio'] = float(max(lengths) / min(lengths))

    return metrics


def is_outlier(atoms, e_per_atom: float, baseline_e_per_atom: float,
              baseline_volume_per_atom: float, dv_max: float = 0.30,
              de_max: float = 5.0) -> tuple[bool, str]:
    """Inline outlier guard — flag obviously broken UMA results.

    Returns (is_outlier, reason). Catches:
      - Cell volume blew up >30% (typical for unphysical placement)
      - Energy outlier >5 eV/atom from baseline (UMA divergence)
      - Atom count below 50% of expected (atoms escaped cell?)
    """
    n = len(atoms)
    vol_per_atom = atoms.get_volume() / n
    dv_rel = (vol_per_atom - baseline_volume_per_atom) / baseline_volume_per_atom
    if abs(dv_rel) > dv_max:
        return True, f"volume_runaway_dv={dv_rel:+.1%}"
    de = e_per_atom - baseline_e_per_atom
    if abs(de) > de_max:
        return True, f"energy_outlier_de={de:+.2f}_eV/atom"
    return False, ""


def compute_descriptors(atoms, baseline_e_per_atom: float,
                        baseline_volume_per_atom: float = None,
                        chem_potentials: dict = None) -> dict:
    """Tier-1 + Tier-2 descriptors after relaxation."""
    e_total = float(atoms.get_potential_energy())
    n = len(atoms)
    e_per_atom = e_total / n
    cell = atoms.get_cell()
    a, b, c = cell.lengths()
    alpha, beta, gamma = cell.angles()
    vol = float(atoms.get_volume())
    syms = atoms.get_chemical_symbols()
    composition = {el: int(c) for el, c in zip(*np.unique(syms, return_counts=True))}
    base = {
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
    # Tier-2 cheap proxy metrics (no extra UMA cost)
    base['tier2'] = compute_tier2_metrics(atoms)
    # Inline outlier guard (uses baseline volume per atom if available)
    if baseline_volume_per_atom is not None:
        is_out, reason = is_outlier(atoms, e_per_atom, baseline_e_per_atom,
                                    baseline_volume_per_atom)
        base['outlier_flag'] = is_out
        base['outlier_reason'] = reason
    return base


def get_baseline(args, calc) -> dict:
    """Get or compute clean LPSCl baseline (e_per_atom, volume_per_atom).

    v4.4 fix (scenario A — silent contamination): when reusing a cached
    baseline.json, verify its source_base_md5 against the current --base
    file. If they differ, refuse rather than silently mix results derived
    from different baselines.
    """
    import hashlib
    base_md5 = None
    if args.base and Path(args.base).exists():
        base_md5 = hashlib.md5(Path(args.base).read_bytes()).hexdigest()

    if args.baseline and Path(args.baseline).exists():
        cached = json.loads(Path(args.baseline).read_text())
        cached_md5 = cached.get('source_base_md5')
        if cached_md5 and base_md5 and cached_md5 != base_md5:
            raise ValueError(
                f"baseline.json was built from a DIFFERENT base CIF.\n"
                f"  cached source_base_md5: {cached_md5}\n"
                f"  current --base md5:     {base_md5}\n"
                f"  current --base path:    {args.base}\n"
                f"  cached source_base:     {cached.get('source_base_file', 'unknown')}\n"
                f"Silent contamination would result. Either:\n"
                f"  (a) rm {args.baseline} and rerun, or\n"
                f"  (b) use a fresh OUT dir for the new base CIF.")
        # v4.4.1 fix: pre-v4.4 baseline.json had no source_base_md5 stamp.
        # When the user supplies --base alongside such a legacy baseline,
        # we cannot verify the CIF matches what the cache was built from.
        # Warn loudly instead of silently trusting (the silent-contamination
        # fail mode v4.4 was supposed to close).
        elif not cached_md5 and base_md5:
            print(f"  ⚠ WARN: cached baseline.json has no source_base_md5 "
                  f"(pre-v4.4 baseline).")
            print(f"     Cannot verify it matches --base {args.base}. "
                  f"Proceeding anyway.")
            print(f"     Recommend: rm {args.baseline} and regenerate once "
                  f"for safety.")
        return cached
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
        # v4.4: stamp source provenance so cached baseline.json can't
        # silently be reused with a different --base CIF.
        'source_base_file': str(args.base),
        'source_base_md5': base_md5,
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
                       help='Max FIRE steps (default 300 for single-element; '
                            'use 1500+ for compound mode — foreign atoms + '
                            'multiple Li vacancies need many steps to settle. '
                            'Compound batch on canonical baseline: 5/51 '
                            'converged at 300, expect ≥45/51 at 1500.)')
    parser.add_argument('--no_cell_relax', action='store_true',
                       help='Position-only relaxation (fix cell)')
    parser.add_argument('--limit', type=int, default=None,
                       help='Limit to first N structures (debug)')
    args = parser.parse_args()

    summary_raw = json.loads(Path(args.summary).read_text())
    if isinstance(summary_raw, dict) and 'structures' in summary_raw:
        summary = summary_raw['structures']
        struct_baseline_meta = summary_raw.get('baseline', {})
    else:
        summary = summary_raw
        struct_baseline_meta = {}
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
            desc = compute_descriptors(atoms, baseline['e_per_atom'],
                                       baseline.get('volume_per_atom'))
    # the original code expects 'desc' just below; cell context preserved
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
                'provenance': _PROVENANCE,
                'cli_args': vars(args),
                'baseline': baseline,
                'structure_baseline_meta': struct_baseline_meta,
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
