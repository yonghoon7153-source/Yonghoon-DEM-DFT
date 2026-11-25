#!/usr/bin/env python
"""uma_screen_all_pairs.py — UMA-based full screening of all enum pairs.

Two-stage workflow:
  Stage 1 (--mode screen): UMA full relax (cell + positions) on best
    champion of each pair. Rank by relaxed energy.
  Stage 2 (--mode eos): UMA EOS scan on top-N pairs (default top 2).
    Birch-Murnaghan fit → V0_BM for DFT sweep recommendation.

This replaces preselection by anneal E_a (which is not fully converged)
with proper UMA full relaxation ranking.

Usage:
  # Stage 1: screen all 26 pairs (~30 min)
  python3 uma_screen_all_pairs.py --mode screen \\
      --enum_dir /scratch/.../1_enumerate/enum_run \\
      --out_dir uma_screen_results

  # Stage 2: EOS on top 2 (auto pick from stage 1, ~20 min)
  python3 uma_screen_all_pairs.py --mode eos \\
      --screen_results uma_screen_results/screen_summary.json \\
      --top_n 2 \\
      --out_dir uma_screen_results

  # Or: combined run (stage 1 + 2 in one shot, ~50 min)
  python3 uma_screen_all_pairs.py --mode all \\
      --enum_dir /scratch/.../1_enumerate/enum_run \\
      --top_n 2 \\
      --out_dir uma_screen_results

Output:
  screen_summary.json — all pairs ranked by UMA relaxed E
  rank{N}_{pair_name}_relaxed.cif — top-N relaxed structures
  eos_results.json — EOS scan + BM fit + DFT recommendation
"""
import argparse
import json
import os
import time
import re
from pathlib import Path
import numpy as np
from ase.io import read, write

# Volume ratio sweep (matches modelC pattern)
VOLUME_RATIOS_DENSE = np.arange(0.92, 1.09, 0.02)  # 9 points: 0.92,...,1.08
VOLUME_RATIOS_DFT = np.arange(0.94, 1.07, 0.02)    # 7 points for DFT

FMAX = 0.05  # eV/Å
NSTEPS = 200


_predictor = None
def make_calc():
    global _predictor
    from fairchem.core import pretrained_mlip
    from fairchem.core.calculate.ase_calculator import FAIRChemCalculator
    if _predictor is None:
        _predictor = pretrained_mlip.get_predict_unit("uma-s-1p1", device="cuda")
    return FAIRChemCalculator(_predictor, task_name="omat")


def list_pair_dirs(enum_dir: Path) -> list[Path]:
    """List all pair_XX_* directories in enum_dir."""
    pairs = sorted(p for p in enum_dir.glob('pair_*') if p.is_dir())
    return pairs


def pick_best_champion(pair_dir: Path, prefer: str = 'lbfgs') -> Path | None:
    """Pick lowest-index champion .cif (lbfgs preferred, else anneal)."""
    cif_files = sorted(pair_dir.glob('*.cif'))
    if not cif_files:
        return None
    lbfgs = [f for f in cif_files if f.name.startswith('lbfgs_')]
    anneal = [f for f in cif_files if f.name.startswith('anneal_')]
    if prefer == 'lbfgs' and lbfgs:
        return sorted(lbfgs)[0]
    elif anneal:
        return sorted(anneal)[0]
    return cif_files[0]


def full_relax(atoms, calc, fmax=FMAX, nsteps=NSTEPS, label=''):
    """Cell + positions full relax."""
    from ase.optimize import LBFGS
    # ASE 3.28+ uses FrechetCellFilter; older versions use ExpCellFilter
    try:
        from ase.filters import FrechetCellFilter as CellFilter
    except ImportError:
        try:
            from ase.constraints import ExpCellFilter as CellFilter
        except ImportError:
            from ase.constraints import UnitCellFilter as CellFilter
    atoms = atoms.copy()
    atoms.calc = calc
    atoms.set_pbc([True, True, True])
    ucf = CellFilter(atoms)
    opt = LBFGS(ucf, logfile=None)
    try:
        opt.run(fmax=fmax, steps=nsteps)
    except Exception as e:
        print(f"    [{label}] relax warning: {e}")
    E = float(atoms.get_potential_energy())
    return E, atoms


def relax_positions_only(atoms, calc, fmax=FMAX, nsteps=NSTEPS, label=''):
    """Position-only relax at fixed cell."""
    from ase.optimize import LBFGS
    atoms = atoms.copy()
    atoms.calc = calc
    atoms.set_pbc([True, True, True])
    opt = LBFGS(atoms, logfile=None)
    try:
        opt.run(fmax=fmax, steps=nsteps)
    except Exception as e:
        print(f"    [{label}] relax warning: {e}")
    E = float(atoms.get_potential_energy())
    return E, atoms


def stage1_screen_all_pairs(enum_dir: Path, out_dir: Path, calc) -> dict:
    """UMA full relax all pairs, rank by E."""
    pairs = list_pair_dirs(enum_dir)
    print(f"\n{'='*70}")
    print(f"STAGE 1: UMA full relax screening — {len(pairs)} pairs")
    print(f"{'='*70}\n")

    results = {}
    t_total = time.time()
    for i, pair_dir in enumerate(pairs, 1):
        cif = pick_best_champion(pair_dir)
        if cif is None:
            print(f"  [{i}/{len(pairs)}] {pair_dir.name}: NO .cif — skip")
            continue
        atoms = read(cif)
        n_atoms = len(atoms)
        V_init = atoms.get_volume()
        t0 = time.time()
        try:
            E, atoms_relaxed = full_relax(atoms, calc, label=pair_dir.name)
            V_final = atoms_relaxed.get_volume()
            dt = time.time() - t0
            results[pair_dir.name] = {
                'pair_dir': str(pair_dir),
                'champion_cif': cif.name,
                'n_atoms': n_atoms,
                'V_init': V_init,
                'V_relaxed': V_final,
                'E_relaxed': E,
                'cell_relaxed': atoms_relaxed.cell.array.tolist(),
                'time_s': dt,
            }
            # Save relaxed structure
            (out_dir / 'relaxed_structures').mkdir(exist_ok=True, parents=True)
            write(out_dir / 'relaxed_structures' / f'{pair_dir.name}_relaxed.cif',
                  atoms_relaxed)
            print(f"  [{i}/{len(pairs)}] {pair_dir.name}: "
                  f"E={E:+.4f} eV  V={V_final:.2f} Å³  ({dt:.1f}s)")
        except Exception as e:
            print(f"  [{i}/{len(pairs)}] {pair_dir.name}: ERROR {e}")
            results[pair_dir.name] = {'pair_dir': str(pair_dir),
                                      'champion_cif': cif.name if cif else None,
                                      'error': str(e)}

    print(f"\nTotal stage 1 time: {(time.time()-t_total)/60:.1f} min")

    # Rank by E
    valid = [(name, r) for name, r in results.items() if 'E_relaxed' in r]
    valid.sort(key=lambda x: x[1]['E_relaxed'])

    print(f"\n--- Ranking (lowest E first) ---")
    print(f"{'rank':>5} {'pair':<30} {'E (eV)':>12} {'V (Å³)':>10} {'n_atoms':>8}")
    print("-" * 70)
    for rank, (name, r) in enumerate(valid, 1):
        print(f"{rank:>5} {name:<30} {r['E_relaxed']:>+12.4f} {r['V_relaxed']:>10.2f} {r['n_atoms']:>8}")

    summary = {
        'enum_dir': str(enum_dir),
        'n_pairs': len(pairs),
        'n_relaxed': len(valid),
        'ranking': [{'rank': i, 'name': name, **r}
                   for i, (name, r) in enumerate(valid, 1)],
        'all_results': results,
    }
    json.dump(summary, open(out_dir / 'screen_summary.json', 'w'),
              indent=2, default=str)
    print(f"\n✓ Saved: {out_dir}/screen_summary.json")
    return summary


def birch_murnaghan(V, V0, B0, B0_prime, E0):
    eta = (V0 / V) ** (2/3)
    return E0 + (9*V0*B0/16) * (
        (eta - 1)**3 * B0_prime
        + (eta - 1)**2 * (6 - 4*eta)
    )


def fit_bm(V_arr, E_arr) -> dict:
    from scipy.optimize import curve_fit
    V_arr = np.asarray(V_arr, float)
    E_arr = np.asarray(E_arr, float)
    i_min = int(np.argmin(E_arr))
    p0 = [V_arr[i_min], 50.0 * 0.006241, 4.0, E_arr[i_min]]
    try:
        popt, _ = curve_fit(birch_murnaghan, V_arr, E_arr, p0=p0, maxfev=20000)
        V0, B0_eV, B0p, E0 = popt
        return {'V0_BM': float(V0),
                'B0_GPa': float(B0_eV / 0.006241),
                'B0_prime': float(B0p),
                'E0_BM': float(E0),
                'fit_success': True}
    except Exception as e:
        return {'V0_BM': V_arr[i_min], 'B0_GPa': None, 'B0_prime': None,
                'E0_BM': E_arr[i_min], 'fit_success': False,
                'fit_error': str(e)}


def stage2_eos_top_n(top_n: int, summary: dict, out_dir: Path, calc) -> dict:
    """Run UMA EOS scan on top-N pairs from stage 1."""
    print(f"\n{'='*70}")
    print(f"STAGE 2: UMA EOS scan on top-{top_n} pairs")
    print(f"{'='*70}\n")

    eos_results = {}
    rel_dir = out_dir / 'relaxed_structures'
    for entry in summary['ranking'][:top_n]:
        pair = entry['name']
        relax_cif = rel_dir / f'{pair}_relaxed.cif'
        if not relax_cif.exists():
            print(f"  Skip {pair} (no relaxed cif found)")
            continue

        atoms_ref = read(relax_cif)
        V_ref = atoms_ref.get_volume()
        E_ref = entry['E_relaxed']
        print(f"\n--- Pair {entry['rank']}: {pair} (V={V_ref:.2f} Å³, E={E_ref:+.4f} eV) ---")

        scan = []
        cell0 = atoms_ref.cell.array.copy()
        for ratio in VOLUME_RATIOS_DENSE:
            scale = ratio ** (1/3)
            atoms = atoms_ref.copy()
            atoms.set_cell(cell0 * scale, scale_atoms=True)
            V = atoms.get_volume()
            t0 = time.time()
            E, _ = relax_positions_only(atoms, calc, label=f"{pair} v{int(100*ratio):03d}")
            dt = time.time() - t0
            scan.append({'ratio': float(ratio), 'V': V, 'E': E, 'time_s': dt})
            print(f"  v{int(100*ratio):03d} (V={V:.2f}): E={E:+.4f} eV  ({dt:.1f}s)")

        bm = fit_bm([p['V'] for p in scan], [p['E'] for p in scan])
        if bm['fit_success']:
            print(f"\n  BM fit: V0={bm['V0_BM']:.3f} Å³, B0={bm['B0_GPa']:.1f} GPa, "
                  f"B0'={bm['B0_prime']:.2f}, E0={bm['E0_BM']:+.4f} eV")
        else:
            print(f"\n  BM fit FAILED: {bm.get('fit_error', '?')}")

        # DFT recommendation
        dft_rec = []
        V0 = bm['V0_BM']
        for r in VOLUME_RATIOS_DFT:
            scale = r ** (1/3)
            dft_rec.append({
                'label': f"v{int(100*r):03d}",
                'ratio': float(r),
                'volume_A3': float(V0 * r),
                'cell_scale': float(scale),
            })
        print(f"\n  DFT EOS sweep (matches modelC v094-v106 pattern):")
        for d in dft_rec:
            print(f"    {d['label']}: V={d['volume_A3']:.2f} Å³, scale={d['cell_scale']:.5f}")

        eos_results[pair] = {
            'rank': entry['rank'],
            'V_ref': V_ref, 'E_ref': E_ref,
            'eos_scan': scan,
            'bm_fit': bm,
            'dft_recommendation': dft_rec,
        }

    json.dump(eos_results, open(out_dir / 'eos_results.json', 'w'),
              indent=2, default=str)
    print(f"\n✓ Saved: {out_dir}/eos_results.json")
    return eos_results


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--mode', choices=['screen', 'eos', 'all'], required=True)
    parser.add_argument('--enum_dir', help='Enum directory (for screen mode)')
    parser.add_argument('--screen_results', help='screen_summary.json (for eos mode)')
    parser.add_argument('--top_n', type=int, default=2, help='Top N pairs for EOS')
    parser.add_argument('--out_dir', default='uma_screen_results')
    args = parser.parse_args()

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    print("="*70)
    print(f"UMA screen + EOS — mode: {args.mode}, top_n: {args.top_n}")
    print("="*70)
    print("Loading UMA-s-1p1...")
    calc = make_calc()
    print("UMA loaded.\n")

    if args.mode in ('screen', 'all'):
        if not args.enum_dir:
            parser.error("--enum_dir required for screen/all mode")
        summary = stage1_screen_all_pairs(Path(args.enum_dir), out_dir, calc)
    elif args.mode == 'eos':
        if not args.screen_results:
            parser.error("--screen_results required for eos mode")
        summary = json.load(open(args.screen_results))

    if args.mode in ('eos', 'all'):
        eos_results = stage2_eos_top_n(args.top_n, summary, out_dir, calc)

    print("\n"+"="*70)
    print("DONE.")
    if args.mode in ('eos', 'all'):
        print(f"\nNext: Use V0_BM from eos_results.json to set up DFT EOS sbatch.")
        for pair_name, r in eos_results.items():
            v0 = r['bm_fit']['V0_BM']
            print(f"  rank{r['rank']} ({pair_name}): V0_BM = {v0:.3f} Å³")


if __name__ == '__main__':
    main()
