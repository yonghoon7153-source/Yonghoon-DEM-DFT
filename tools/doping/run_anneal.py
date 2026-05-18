#!/usr/bin/env python
"""run_anneal.py — Pipeline Step 3: Li-selective thermal annealing.

Takes champion candidate structures from screening and runs MLIP MD at
500 K for tens of ps. At 500 K Li⁺ hops actively (Eₐ ≈ 0.2 eV << kT = 0.043
eV) while PS₄ framework (P-S ≈ 3.5 eV) and the Cl⁻ cage stay rigid — i.e.,
we re-optimize only the Li sublattice while keeping the anion arrangement
fixed (D'Amore 2022, Pustorino 2025 ordering ↔ B0 evidence).

After MD, a final UMA relax (FIRE) gives the post-anneal energy. Compare
to the pre-anneal energy from screening to see whether the deeper basin
shifted the candidate ranking — Pipeline doc cites a Li6PS5Cl example
where screening 4th → anneal 1st.

Usage:
  # Anneal a hand-picked list of xyz files (one per champion).
  python3 run_anneal.py \\
      --xyz path/to/Nd2O3_x050_s00.xyz path/to/La2O3_x050_s00.xyz ... \\
      --out runs/anneal_top5_2026_05_15/ \\
      --temperature 500 --time_ps 50

  # Or pull the top-N candidates straight from analyze_screening output.
  python3 run_anneal.py \\
      --top_candidates runs/.../top_candidates_v2.json \\
      --top 5 --out runs/anneal_top5_2026_05_15/
"""
import argparse
import json
import sys
import time
from pathlib import Path
import numpy as np
from ase.io import read, write
from ase.md.langevin import Langevin
from ase.md.velocitydistribution import MaxwellBoltzmannDistribution
from ase.optimize import FIRE
from ase import units

sys.path.insert(0, str(Path(__file__).parent))
from _provenance import get_provenance

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


def winner_name(xyz_path):
    """v4.5.18 NEW-D defensive fix: cascade outputs share stem
    'post_relax' or 'post_md' across winners. Use parent dir name in
    that case. Same pattern as bvse_proxy/run_mlip_postproc (v4.5.17)
    + combine_rankings.py CR-A (v4.5.8). Round 3 reviewer flagged this
    as 'conditional hole — safe in current cascade flow but manual
    re-anneal of post_relax.xyz would collide'. Defensive patch."""
    p = Path(xyz_path)
    if p.stem in ('post_relax', 'post_md'):
        return p.parent.name
    return p.stem


def anneal_one(xyz_path: Path, calc, out_dir: Path,
              temperature_K: float = 500, time_ps: float = 50,
              dt_fs: float = 2.0, friction: float = 0.01,
              relax_steps: int = 1500, relax_fmax: float = 0.05,
              cell_relax: bool = True, log_every: int = 500) -> dict:
    """Run Langevin NVT MD at ``temperature_K`` for ``time_ps``, then a final
    cell+positions relax. Records pre-anneal, post-MD, and post-relax energies
    so you can see how much extra binding the thermal sampling found."""
    name = winner_name(xyz_path)
    work = out_dir / name
    work.mkdir(parents=True, exist_ok=True)

    atoms = read(str(xyz_path))
    atoms.calc = calc
    E_pre = float(atoms.get_potential_energy())
    n_atoms = len(atoms)

    # Initialize Maxwell-Boltzmann velocities
    MaxwellBoltzmannDistribution(atoms, temperature_K=temperature_K)

    n_steps = int(time_ps * 1000 / dt_fs)
    print(f"  [{name}] MD: T={temperature_K}K, dt={dt_fs}fs, "
          f"steps={n_steps} ({time_ps}ps), {n_atoms} atoms")

    md_log = work / 'md.log'
    md_traj = work / 'md.traj'
    dyn = Langevin(atoms, dt_fs * units.fs,
                   temperature_K=temperature_K,
                   friction=friction,
                   logfile=str(md_log),
                   trajectory=str(md_traj),
                   loginterval=log_every)

    t0 = time.time()
    dyn.run(n_steps)
    t_md = time.time() - t0
    E_md_final = float(atoms.get_potential_energy())
    print(f"  [{name}] MD done ({t_md:.1f}s) "
          f"E_pre={E_pre/n_atoms:.4f} → E_md={E_md_final/n_atoms:.4f} eV/atom")

    # Save post-MD snapshot
    write(work / 'post_md.xyz', atoms)

    # Final relax
    target = CellFilter(atoms) if cell_relax else atoms
    opt = FIRE(target, logfile=str(work / 'relax.log'))
    t0 = time.time()
    opt.run(fmax=relax_fmax, steps=relax_steps)
    t_relax = time.time() - t0
    n_relax_steps = opt.get_number_of_steps()
    converged = n_relax_steps < relax_steps
    E_post = float(atoms.get_potential_energy())
    write(work / 'post_relax.xyz', atoms)

    delta_E_per_atom = (E_post - E_pre) / n_atoms
    print(f"  [{name}] relax {n_relax_steps} steps ({t_relax:.1f}s) "
          f"E_post={E_post/n_atoms:.4f} eV/atom, "
          f"ΔE_anneal={delta_E_per_atom*1000:+.1f} meV/atom, "
          f"conv={converged}")

    return {
        'name': name,
        'xyz_input': str(xyz_path),
        'n_atoms': n_atoms,
        'temperature_K': temperature_K,
        'time_ps': time_ps,
        'dt_fs': dt_fs,
        'E_pre_anneal': E_pre,
        'E_md_final': E_md_final,
        'E_post_relax': E_post,
        'delta_E_anneal_meV_per_atom': delta_E_per_atom * 1000,
        'cell_pre': read(str(xyz_path)).cell.array.tolist(),
        'cell_post': atoms.cell.array.tolist(),
        'volume_pre': float(read(str(xyz_path)).get_volume()),
        'volume_post': float(atoms.get_volume()),
        't_md_s': t_md,
        't_relax_s': t_relax,
        'n_relax_steps': n_relax_steps,
        'converged': converged,
        'post_md_xyz': str(work / 'post_md.xyz'),
        'post_relax_xyz': str(work / 'post_relax.xyz'),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                    formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--xyz', nargs='+',
                       help='xyz files to anneal (one or more)')
    parser.add_argument('--xyz_dir',
                       help='Directory of xyz files to anneal — recursive '
                            'glob "**/*.xyz". Use for "anneal ALL screening '
                            'candidates" mode since UMA pre-anneal ranking is '
                            'a heuristic and Pipeline Step 3 docs note '
                            'screening can re-order under anneal.')
    parser.add_argument('--summary_json',
                       help='Structures summary JSON (substitute_compound '
                            "output); pulls xyz_file from each entry's "
                            "'xyz_file' field. Alternative to --xyz_dir for "
                            'a specific batch.')
    parser.add_argument('--top_candidates',
                       help='analyze_screening top_candidates JSON; pulls '
                            'xyz_file path from each record')
    parser.add_argument('--top', type=int, default=5,
                       help='If --top_candidates: number of top entries to anneal')
    parser.add_argument('--per_compound_top', type=int, default=None,
                       help='Per-compound stratified Top-N anneal: groups the '
                            'input (from --summary_json or --uma_results) by '
                            "dopant, anneals the lowest-ΔE/atom N entries of "
                            "each group. Recommended for compound batches "
                            "where ranking is heavy-tailed (one strong cation "
                            "family dominates the global Top-N otherwise).")
    parser.add_argument('--uma_results',
                       help='UMA screening results JSON (has uma_relaxed.'
                            'de_per_atom_vs_baseline per record). Used as '
                            'sort key when --per_compound_top is set.')
    parser.add_argument('--light', action='store_true',
                       help='Light anneal preset (300K, 20 ps, 500 relax '
                            'steps) — for stratified per-compound Top-N to '
                            'cheaply relieve unphysical Li placement before '
                            'reranking. Override individual flags as needed.')
    parser.add_argument('--out', required=True, help='Output base directory')
    parser.add_argument('--temperature', type=float, default=500,
                       help='Annealing temperature in K (default 500; pipeline '
                            'doc cites Li hop Eₐ~0.2 eV, kT@500K=0.043 eV; '
                            'avoid >800K — Cl cage starts to break)')
    parser.add_argument('--time_ps', type=float, default=50,
                       help='MD duration in ps (default 50; 25 ps minimum '
                            'for Li sub-lattice equilibration)')
    parser.add_argument('--dt_fs', type=float, default=2.0,
                       help='MD time step in fs')
    parser.add_argument('--friction', type=float, default=0.01,
                       help='Langevin friction (ase units)')
    parser.add_argument('--relax_steps', type=int, default=1500,
                       help='Post-MD FIRE max steps (default 1500 to match '
                            'compound-substitution screening)')
    parser.add_argument('--relax_fmax', type=float, default=0.05)
    parser.add_argument('--no_cell_relax', action='store_true',
                       help='Position-only final relax (fix cell)')
    parser.add_argument('--device', default='cuda')
    parser.add_argument('--task', default='omat')
    parser.add_argument('--log_every', type=int, default=500,
                       help='MD log interval (steps)')
    args = parser.parse_args()

    if not args.xyz and not args.top_candidates and not args.summary_json and not args.xyz_dir:
        parser.error("Provide --xyz files, --xyz_dir, --top_candidates, or --summary_json JSON")

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    # Build xyz list (multiple input modes)
    if args.xyz:
        xyz_paths = [Path(p) for p in args.xyz]
    elif args.xyz_dir:
        xyz_paths = sorted(Path(args.xyz_dir).rglob('*.xyz'))
        # Filter out anneal-produced (post_md.xyz, post_relax.xyz) to avoid
        # re-annealing our own outputs if --xyz_dir overlaps --out
        xyz_paths = [p for p in xyz_paths
                     if p.name not in ('post_md.xyz', 'post_relax.xyz')]
        print(f"  Discovered {len(xyz_paths)} xyz files under {args.xyz_dir}")
    elif args.summary_json:
        data = json.loads(Path(args.summary_json).read_text())
        # Accept the key conventions used by upstream tools:
        #   substitute_compound output → {'structures': [...]}
        #   run_uma_screening output   → {'results':    [...]}
        #   select_winners output      → {'winners':    [...]}  (cascade Stage 03)
        recs = (data.get('winners')
                or data.get('structures')
                or data.get('results', [])
                if isinstance(data, dict) else data)
        xyz_paths = [Path(r['xyz_file']) for r in recs
                     if 'xyz_file' in r and Path(r['xyz_file']).exists()]
        print(f"  Loaded {len(xyz_paths)} xyz from summary {args.summary_json}")
    elif args.top_candidates:
        data = json.loads(Path(args.top_candidates).read_text())
        top = data.get('top_candidates', [])[:args.top]
        xyz_paths = []
        for entry in top:
            xpath = entry.get('xyz_file')
            if xpath and Path(xpath).exists():
                xyz_paths.append(Path(xpath))
            else:
                print(f"  ⚠ skip {entry.get('name')}: xyz_file not found "
                      f"({xpath})")
    else:
        parser.error("Provide --xyz, --xyz_dir, --summary_json, or --top_candidates")
    if not xyz_paths:
        raise SystemExit("No xyz files found")

    # Per-compound stratified Top-N filter
    if args.per_compound_top:
        if not args.uma_results:
            parser.error("--per_compound_top requires --uma_results "
                        "(needs ΔE/atom for ranking within each dopant group)")
        uma = json.loads(Path(args.uma_results).read_text())['results']
        # Map xyz path → ΔE/atom + dopant
        name_to_xpath = {winner_name(p): p for p in xyz_paths}
        from collections import defaultdict
        groups = defaultdict(list)
        for rec in uma:
            name = rec.get('name')
            if name in name_to_xpath:
                groups[rec.get('dopant', 'unknown')].append((
                    rec['uma_relaxed']['de_per_atom_vs_baseline'],
                    name_to_xpath[name],
                ))
        filtered: list = []
        for dop, items in groups.items():
            items.sort()  # ascending ΔE → most stable first
            keep = items[:args.per_compound_top]
            filtered.extend(p for _, p in keep)
            print(f"  per-compound Top-{args.per_compound_top}: {dop} → "
                  f"{len(keep)}/{len(items)}")
        xyz_paths = filtered
        print(f"  Stratified Top-{args.per_compound_top}: "
              f"{len(xyz_paths)} structures across {len(groups)} dopants")

    # --light preset
    if args.light:
        args.temperature = min(args.temperature, 300)
        args.time_ps = min(args.time_ps, 20)
        args.relax_steps = min(args.relax_steps, 500)
        print(f"  --light preset: T={args.temperature}K, "
              f"t={args.time_ps}ps, relax steps={args.relax_steps}")

    print(f"Loading UMA-s-1p1 ({args.device})...")
    calc = load_uma_calc(args.device, args.task)

    # Existing results (resume support)
    results_path = out / 'anneal_results.json'
    done = {}
    if results_path.exists():
        existing = json.loads(results_path.read_text())
        done = {r['name']: r for r in existing.get('results', [])}
        print(f"Resume: {len(done)} already annealed")

    todo = [p for p in xyz_paths if winner_name(p) not in done]
    print(f"To process: {len(todo)}/{len(xyz_paths)}")

    results = list(done.values())
    t_start = time.time()
    for i, p in enumerate(todo):
        print(f"\n[{i+1}/{len(todo)}] {winner_name(p)}")
        try:
            rec = anneal_one(
                p, calc, out,
                temperature_K=args.temperature,
                time_ps=args.time_ps,
                dt_fs=args.dt_fs,
                friction=args.friction,
                relax_steps=args.relax_steps,
                relax_fmax=args.relax_fmax,
                cell_relax=not args.no_cell_relax,
                log_every=args.log_every,
            )
            results.append(rec)
        except Exception as e:
            print(f"  ❌ FAILED: {e}")
            results.append({'name': winner_name(p), 'xyz_input': str(p),
                           'error': str(e)})
        # Periodic save
        if (i + 1) % 2 == 0 or (i + 1) == len(todo):
            results_path.write_text(json.dumps({
                'provenance': get_provenance(),
                'temperature_K': args.temperature,
                'time_ps': args.time_ps,
                'n_done': len(results),
                'results': results,
            }, indent=2, default=str))

    # Final summary
    print(f"\n{'='*68}")
    print(f"{'Champion':<35}{'E_pre':>10}{'E_post':>10}{'ΔE meV/at':>12}")
    print('-' * 68)
    for r in sorted([x for x in results if 'error' not in x],
                   key=lambda x: x.get('delta_E_anneal_meV_per_atom', 0)):
        nat = r.get('n_atoms', 1)
        ep = r.get('E_pre_anneal', 0) / nat
        epo = r.get('E_post_relax', 0) / nat
        de = r.get('delta_E_anneal_meV_per_atom', 0)
        print(f"{r['name']:<35}{ep:>+10.4f}{epo:>+10.4f}{de:>+10.1f}")
    print('=' * 68)
    print(f"Total: {time.time() - t_start:.1f}s")
    print(f"Results: {results_path}")


if __name__ == '__main__':
    main()
