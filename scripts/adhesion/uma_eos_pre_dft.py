#!/usr/bin/env python
"""uma_eos_pre_dft.py — UMA-based EOS for V0 estimation before DFT sweep.

Workflow:
  1. Read champion .cif files for rank1 (pair_00) and rank2 (pair_24)
  2. Pick lowest-E_a champion per rank (auto-detect from category, or explicit)
  3. UMA relax positions only (fixed cell) at multiple V/V0 ratios
  4. Birch-Murnaghan EOS fit → V0, B0, E0
  5. Output recommended DFT volumes (v094 ~ v106) compatible with existing pipeline

Run on KISTI Olaf with (uma) env activated:
  python3 uma_eos_pre_dft.py --rank1-dir /scratch/.../pair_00_reference_1_82 \\
                              --rank2-dir /scratch/.../pair_24_cross_15_75 \\
                              --out_dir uma_eos_results

Cost: ~10-20 min on 1 GPU per rank (11 volumes × ~1 min each).
"""
import argparse
import json
import os
import time
from pathlib import Path
import numpy as np
from ase.io import read, write

# Volume ratio sweep (matches modelC pattern: v094, v096, ..., v106)
VOLUME_RATIOS = np.arange(0.94, 1.07, 0.02)  # 0.94, 0.96, ..., 1.06 → 7 points
# Use higher density for good BM fit
VOLUME_RATIOS_DENSE = np.arange(0.92, 1.09, 0.02)  # 9 points

# UMA relax convergence
FMAX = 0.05  # eV/Å (tight enough for EOS)
NSTEPS = 200


_predictor = None
def make_calc():
    global _predictor
    from fairchem.core import pretrained_mlip
    from fairchem.core.calculate.ase_calculator import FAIRChemCalculator
    if _predictor is None:
        _predictor = pretrained_mlip.get_predict_unit("uma-s-1p1", device="cuda")
    return FAIRChemCalculator(_predictor, task_name="omat")


def pick_best_champion(pair_dir: Path, prefer: str = 'lbfgs') -> Path:
    """Pick lowest-E champion .cif from pair_XX directory.

    Strategy:
      1. Prefer 'lbfgs_*' files (post-relaxation, more reliable).
      2. Within lbfgs, pick lowest filename suffix (often = lowest energy).
      3. Fallback to 'anneal_*' if no lbfgs files.

    Returns: path to selected .cif
    """
    cif_files = sorted(pair_dir.glob('*.cif'))
    if not cif_files:
        raise FileNotFoundError(f"No .cif files in {pair_dir}")

    lbfgs = [f for f in cif_files if f.name.startswith('lbfgs_')]
    anneal = [f for f in cif_files if f.name.startswith('anneal_')]

    if prefer == 'lbfgs' and lbfgs:
        chosen = sorted(lbfgs)[0]  # lowest index typically lowest E
    elif anneal:
        chosen = sorted(anneal)[0]
    else:
        chosen = cif_files[0]

    print(f"  Champions in {pair_dir.name}:")
    for f in cif_files:
        marker = ' ← chosen' if f == chosen else ''
        print(f"    {f.name}{marker}")
    return chosen


def relax_positions_only(atoms, calc, fmax=FMAX, nsteps=NSTEPS, label=''):
    """Relax atomic positions at fixed cell, return final energy."""
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


def scan_volume(atoms_ref, calc, ratios=VOLUME_RATIOS_DENSE, label='') -> dict:
    """Scan V/V0 ratios, relax positions at each, return E(V) curve."""
    cell0 = atoms_ref.cell.array.copy()
    V0 = atoms_ref.get_volume()
    print(f"  Reference V0 = {V0:.3f} Å³ ({len(atoms_ref)} atoms)")

    results = []
    for ratio in ratios:
        scale = ratio ** (1/3)
        atoms = atoms_ref.copy()
        atoms.set_cell(cell0 * scale, scale_atoms=True)
        V = atoms.get_volume()
        t0 = time.time()
        E, atoms_relaxed = relax_positions_only(atoms, calc, label=f"{label} v{int(100*ratio):03d}")
        dt = time.time() - t0
        print(f"    v{int(100*ratio):03d} (V={V:.2f} Å³): E={E:+.4f} eV  ({dt:.1f}s)")
        results.append({'ratio': float(ratio), 'V': float(V), 'E': float(E), 'time_s': dt})
    return {'V0_input': float(V0), 'cell0': cell0.tolist(), 'curve': results}


def birch_murnaghan(V, V0, B0, B0_prime, E0):
    """Birch-Murnaghan 3rd-order EOS."""
    eta = (V0 / V) ** (2/3)
    return E0 + (9*V0*B0/16) * (
        (eta - 1)**3 * B0_prime
        + (eta - 1)**2 * (6 - 4*eta)
    )


def fit_birch_murnaghan(V_arr, E_arr) -> dict:
    """Fit BM3 EOS to (V, E) data. Returns V0, B0, B0', E0."""
    from scipy.optimize import curve_fit
    V_arr = np.asarray(V_arr, float)
    E_arr = np.asarray(E_arr, float)
    # Initial guess: parabolic minimum
    i_min = int(np.argmin(E_arr))
    V0_init = V_arr[i_min]
    E0_init = E_arr[i_min]
    B0_init = 50.0  # GPa typical for oxides — fit will refine. But careful with units!
    # Convert: B0 in eV/Å³ for fit (1 GPa = 0.006241 eV/Å³)
    B0_init_eV = 50.0 * 0.006241
    B0p_init = 4.0
    try:
        popt, pcov = curve_fit(
            birch_murnaghan, V_arr, E_arr,
            p0=[V0_init, B0_init_eV, B0p_init, E0_init],
            maxfev=20000,
        )
        V0, B0_eV, B0p, E0 = popt
        B0_GPa = B0_eV / 0.006241
        return {
            'V0_BM': float(V0), 'B0_GPa': float(B0_GPa), 'B0_prime': float(B0p),
            'E0_BM': float(E0), 'fit_success': True,
        }
    except Exception as e:
        print(f"    BM fit failed: {e}")
        return {'V0_BM': V0_init, 'B0_GPa': None, 'B0_prime': None,
                'E0_BM': E0_init, 'fit_success': False}


def recommend_dft_range(V0_BM: float, ratios=VOLUME_RATIOS) -> list[dict]:
    """Generate DFT volume sweep recommendation using V0_BM as reference."""
    rec = []
    for r in ratios:
        scale = r ** (1/3)
        V = V0_BM * r
        rec.append({'label': f"v{int(100*r):03d}", 'ratio': float(r),
                    'volume_A3': float(V), 'cell_scale': float(scale)})
    return rec


def process_rank(rank_label: str, pair_dir: Path, calc, out_dir: Path) -> dict:
    print(f"\n{'='*70}")
    print(f"Processing {rank_label}: {pair_dir.name}")
    print(f"{'='*70}")
    cif = pick_best_champion(pair_dir)
    atoms = read(cif)
    print(f"\n  Loaded {cif.name} ({len(atoms)} atoms)")

    # First: relax fully (cell + positions) to get clean V0
    print(f"\n  Step 1: Full relax (cell + positions) at reference volume...")
    from ase.optimize import LBFGS
    from ase.constraints import ExpCellFilter
    atoms_full = atoms.copy()
    atoms_full.calc = calc
    atoms_full.set_pbc([True, True, True])
    ucf = ExpCellFilter(atoms_full)
    opt = LBFGS(ucf, logfile=None)
    t0 = time.time()
    opt.run(fmax=FMAX, steps=NSTEPS)
    E_ref = float(atoms_full.get_potential_energy())
    V_ref = atoms_full.get_volume()
    print(f"  Ref relax: V_ref = {V_ref:.3f} Å³, E_ref = {E_ref:+.4f} eV ({(time.time()-t0):.1f}s)")

    # Save relaxed structure
    write(out_dir / f"{rank_label}_relaxed.cif", atoms_full)

    # Second: V scan at fixed cell (positions only)
    print(f"\n  Step 2: Volume scan ±8% ({len(VOLUME_RATIOS_DENSE)} points)...")
    scan = scan_volume(atoms_full, calc, ratios=VOLUME_RATIOS_DENSE, label=rank_label)
    V_arr = [p['V'] for p in scan['curve']]
    E_arr = [p['E'] for p in scan['curve']]

    # BM fit
    print(f"\n  Step 3: Birch-Murnaghan EOS fit...")
    bm = fit_birch_murnaghan(V_arr, E_arr)
    if bm['fit_success']:
        print(f"    V0_BM    = {bm['V0_BM']:.3f} Å³")
        print(f"    B0       = {bm['B0_GPa']:.1f} GPa")
        print(f"    B0_prime = {bm['B0_prime']:.2f}")
        print(f"    E0_BM    = {bm['E0_BM']:.4f} eV")

    # DFT recommendation
    print(f"\n  Step 4: DFT EOS sweep recommendation (matches modelC v094-v106 pattern)...")
    rec = recommend_dft_range(bm['V0_BM'], ratios=VOLUME_RATIOS)
    for r in rec:
        print(f"    {r['label']}: V = {r['volume_A3']:.2f} Å³, cell scale = {r['cell_scale']:.5f}")

    return {
        'rank': rank_label,
        'pair_dir': str(pair_dir),
        'champion_cif': str(cif),
        'V_ref_relaxed': V_ref,
        'E_ref_relaxed': E_ref,
        'cell_relaxed': atoms_full.cell.array.tolist(),
        'eos_scan': scan,
        'bm_fit': bm,
        'dft_recommendation': rec,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--rank1-dir', required=True, help='pair_00 (or whatever rank1) directory')
    parser.add_argument('--rank2-dir', required=True, help='pair_24 (or whatever rank2) directory')
    parser.add_argument('--out_dir', default='uma_eos_results', help='Output dir')
    args = parser.parse_args()

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 70)
    print("UMA EOS pre-DFT analysis — V0 + sweep range estimation")
    print("=" * 70)
    print(f"Rank1: {args.rank1_dir}")
    print(f"Rank2: {args.rank2_dir}")
    print(f"Output: {out_dir}/")
    print(f"\nLoading UMA-s-1p1 (cuda)...")
    calc = make_calc()
    print(f"UMA loaded.\n")

    results = {}
    results['rank1'] = process_rank('rank1', Path(args.rank1_dir), calc, out_dir)
    results['rank2'] = process_rank('rank2', Path(args.rank2_dir), calc, out_dir)

    # Save full results
    json.dump(results, open(out_dir / 'uma_eos_results.json', 'w'), indent=2, default=str)
    print(f"\n{'='*70}")
    print(f"Full results saved: {out_dir}/uma_eos_results.json")
    print(f"Relaxed structures: {out_dir}/rank{1,2}_relaxed.cif")
    print(f"{'='*70}")
    print(f"\nNext step: Use V0_BM values to set up DFT EOS sweep on KISTI sbatch.")
    print(f"  rank1 V0_BM = {results['rank1']['bm_fit']['V0_BM']:.3f} Å³")
    print(f"  rank2 V0_BM = {results['rank2']['bm_fit']['V0_BM']:.3f} Å³")


if __name__ == '__main__':
    main()
