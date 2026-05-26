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
# Narrow grid v097..v105 (-3%..+5%, 1% steps, 9 pts). Wider ranges hit
# extreme-strain basin jumps (Li rearranges at ~-4% / large +%); this window
# was verified smooth in the continuation run, giving a clean single-basin BM3.
VOLUME_RATIOS_DENSE = np.round(np.arange(0.97, 1.055, 0.01), 2)  # 0.97..1.05 → 9 points

# UMA model — match Nd anneal champion relax (modelc_nd_doped.json: UMA-s-1p2).
# If the KISTI/gabia uma env only has 1p1, change this one line back to "uma-s-1p1".
UMA_MODEL = "uma-s-1p2"

# UMA relax convergence
FMAX = 0.05      # eV/Å — (legacy) loose relax
REF_FMAX = 0.01  # tight cell+pos vc-relax → accurate equilibrium V0 cell (the goal)
NSTEPS = 300
EOS_FMAX = 0.01  # tighter per-volume relax → smooth E(V) (avoids basin-jump noise)


_predictor = None
def make_calc():
    global _predictor
    from fairchem.core import pretrained_mlip
    from fairchem.core.calculate.ase_calculator import FAIRChemCalculator
    if _predictor is None:
        _predictor = pretrained_mlip.get_predict_unit(UMA_MODEL, device="cuda")
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


def scan_volume(atoms_ref, calc, ratios=VOLUME_RATIOS_DENSE, label='', fmax=EOS_FMAX) -> dict:
    """Scan V/V0 ratios with CONTINUATION relaxation, return E(V) curve.

    Start from the relaxed reference at V0 and step OUTWARD in both directions
    (V0 -> expansion, V0 -> compression), seeding each volume from the previous
    relaxed structure (fractional coords carried via scale_atoms). This keeps
    mobile Li in the same basin across volumes -> smooth E(V). Independent
    per-volume relax (old behaviour) can jump basins at strained volumes and
    produce kinks (e.g. a downward spike at +4%) that corrupt the BM3 B0'.
    """
    cell0 = atoms_ref.cell.array.copy()
    V0 = atoms_ref.get_volume()
    rs = sorted(float(r) for r in ratios)
    i0 = min(range(len(rs)), key=lambda i: abs(rs[i] - 1.0))
    print(f"  Reference V0 = {V0:.3f} Å³ ({len(atoms_ref)} atoms); "
          f"continuation scan from v{int(round(100*rs[i0])):03d}, fmax={fmax}")
    out = {}

    def _do(i, seed):
        scale = rs[i] ** (1/3)
        atoms = seed.copy()
        atoms.set_cell(cell0 * scale, scale_atoms=True)  # carry seed fractional coords
        V = atoms.get_volume()
        t0 = time.time()
        vlabel = f"v{int(round(100*rs[i])):03d}"
        E, relaxed = relax_positions_only(atoms, calc, fmax=fmax, label=f"{label} {vlabel}")
        dt = time.time() - t0
        print(f"    {vlabel} (V={V:.2f} Å³): E={E:+.4f} eV  ({dt:.1f}s)")
        out[i] = {'ratio': rs[i], 'V': float(V), 'E': float(E), 'time_s': dt}
        return relaxed

    seed = atoms_ref
    for i in range(i0, len(rs)):      # expand outward
        seed = _do(i, seed)
    seed = atoms_ref
    for i in range(i0 - 1, -1, -1):   # compress outward
        seed = _do(i, seed)

    results = [out[i] for i in range(len(rs))]
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
        rec.append({'label': f"v{int(round(100*r)):03d}", 'ratio': float(r),
                    'volume_A3': float(V), 'cell_scale': float(scale)})
    return rec


def load_structure(structure=None, pair_dir=None):
    """Load a start structure: QE input (.in/.pwi, robust), QE output, or champion dir."""
    if structure:
        if structure.endswith(('.in', '.pwi')):
            return read(structure, format='espresso-in')
        try:
            return read(structure, index=-1)
        except Exception:
            return read(structure, index=-1, format='espresso-out')
    return read(pick_best_champion(Path(pair_dir)))


def process_rank(rank_label: str, calc, out_dir: Path,
                 structure: str = None, pair_dir: str = None, atoms_in=None) -> dict:
    print(f"\n{'='*70}")
    print(f"Processing {rank_label}")
    print(f"{'='*70}")
    if atoms_in is not None:
        atoms = atoms_in.copy()
        src = '(in-memory seed)'
        print(f"\n  Using in-memory structure ({len(atoms)} atoms)")
    elif structure:
        # Start from an explicit structure file.
        #  - QE input (.in/.pwi): clean cell+coords, no eigenvalues → robust.
        #  - QE output (.out/.pwo): ASE's espresso-out parser asserts on
        #    incomplete / spin-polarized band data (common for scancelled or
        #    DFT+U+ISPIN=2 runs), so prefer the .in.
        src = structure
        if structure.endswith(('.in', '.pwi')):
            atoms = read(structure, format='espresso-in')
        else:
            try:
                atoms = read(structure, index=-1)
            except Exception:
                atoms = read(structure, index=-1, format='espresso-out')
        print(f"\n  Loaded structure from {src} ({len(atoms)} atoms)")
    else:
        cif = pick_best_champion(Path(pair_dir))
        src = str(cif)
        atoms = read(cif)
        print(f"\n  Loaded {cif.name} ({len(atoms)} atoms)")

    # Step 1: ion-relax at the INPUT cell (cell SHAPE held fixed — preserve the
    # argyrodite framework; NO vc-relax, which would let the lattice distort off
    # the parent symmetry). The EOS then scans ISOTROPIC volume scalings of this
    # cell, so only the volume (V0) is fit from E(V); cell shape is preserved.
    print(f"\n  Step 1: ion-relax at fixed input cell, fmax={REF_FMAX}...")
    from ase.geometry import cell_to_cellpar
    t0 = time.time()
    E_ref, atoms_full = relax_positions_only(atoms, calc, fmax=REF_FMAX,
                                             nsteps=NSTEPS, label=rank_label)
    V_ref = atoms_full.get_volume()
    cellpar = [float(x) for x in cell_to_cellpar(atoms_full.cell.array)]
    cif_path = out_dir / f"{rank_label}_relaxed.cif"
    write(cif_path, atoms_full)
    print(f"  V_ref={V_ref:.3f} Å³ (cell shape fixed)  E_ref={E_ref:+.4f} eV  "
          f"a,b,c={cellpar[0]:.4f},{cellpar[1]:.4f},{cellpar[2]:.4f} ({(time.time()-t0):.1f}s)")

    result = {
        'rank': rank_label,
        'start_structure': src,
        'uma_model': UMA_MODEL,
        'V_ref_relaxed': V_ref,
        'E_ref_relaxed': E_ref,
        'cell_relaxed': atoms_full.cell.array.tolist(),
        'cellpar': cellpar,
        'relaxed_cif': str(cif_path),
        'eos_scan': None,
        'bm_fit': {'fit_success': False, 'V0_BM': V_ref,
                   'B0_GPa': None, 'B0_prime': None, 'E0_BM': E_ref},
    }

    # Step 2-3: EOS — isotropic volume scan (shape fixed) + ion-relax + BM3 fit
    print(f"\n  Step 2: Volume scan ({len(VOLUME_RATIOS_DENSE)} points, continuation, isotropic)...")
    scan = scan_volume(atoms_full, calc, ratios=VOLUME_RATIOS_DENSE, label=rank_label)
    bm = fit_birch_murnaghan([p['V'] for p in scan['curve']],
                             [p['E'] for p in scan['curve']])
    if bm['fit_success']:
        print(f"    V0_BM={bm['V0_BM']:.3f} Å³  B0={bm['B0_GPa']:.1f} GPa  B0'={bm['B0_prime']:.2f}")
    result.update({'eos_scan': scan, 'bm_fit': bm,
                   'dft_recommendation': recommend_dft_range(bm['V0_BM'], ratios=VOLUME_RATIOS)})
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--rank1-dir', help='rank1 champion dir (picks best .cif)')
    parser.add_argument('--rank2-dir', help='rank2 champion dir (optional)')
    parser.add_argument('--rank1-structure', help='rank1 explicit structure file, e.g. a '
                        'DFT relax.out (final coords used); overrides --rank1-dir')
    parser.add_argument('--rank2-structure', help='rank2 explicit structure file (optional)')
    parser.add_argument('--out_dir', default='uma_eos_results', help='Output dir')
    parser.add_argument('--n_seeds', type=int, default=1,
                        help='ensemble: N rattled seeds (rank1 only) → B0 mean±std')
    parser.add_argument('--perturb', type=float, default=0.1,
                        help='rattle stdev (Å) applied to seeds>0')
    args = parser.parse_args()
    if not (args.rank1_dir or args.rank1_structure):
        parser.error('provide --rank1-structure or --rank1-dir')

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

    if args.n_seeds > 1:
        # ENSEMBLE (rank1 only): rattle start → full relax → EOS → BM3, per seed.
        # Robust B0 for soft / Li-mobile / vacancy structures (single curve is
        # basin-sensitive). Report mean±std over seeds.
        # ALL seeds do the FULL EOS. V0 = BM3 parabola minimum (project standard:
        # CODE_INVENTORY pipeline-v2 step 4 & 6 — MLIP EOS → BM3 → V0 → V0.xyz).
        # Ensemble → converged V0 ± std; champion = deepest minimum (lowest E0_BM).
        print(f"\n=== ENSEMBLE: {args.n_seeds} seeds, rattle {args.perturb} Å (rank1, full EOS) ===")
        base = load_structure(args.rank1_structure, args.rank1_dir)
        seed_res = []
        for s in range(args.n_seeds):
            a = base.copy()
            if s > 0:
                a.rattle(stdev=args.perturb, seed=s)
            r = process_rank(f'rank1_seed{s}', calc, out_dir, atoms_in=a)
            seed_res.append(r)
            json.dump({'rank1_ensemble': seed_res},  # incremental (survive walltime kill)
                      open(out_dir / 'uma_eos_results.json', 'w'), indent=2, default=str)

        ok = [r for r in seed_res
              if r['bm_fit']['fit_success'] and r['bm_fit']['B0_GPa'] is not None]
        if not ok:
            print("\n[no successful BM fits]"); print('='*70); return
        V0s = np.array([r['bm_fit']['V0_BM'] for r in ok])
        B0s = np.array([r['bm_fit']['B0_GPa'] for r in ok])
        # champion = deepest EOS minimum (lowest E0_BM) = best ground state
        champ = min(ok, key=lambda r: r['bm_fit']['E0_BM'])
        cbm = champ['bm_fit']
        # cell at champion V0 = relaxed reference cell scaled to V0_BM (isotropic EOS)
        from ase.geometry import cell_to_cellpar
        scale = (cbm['V0_BM'] / champ['V_ref_relaxed']) ** (1.0 / 3.0)
        cp = cell_to_cellpar(np.array(champ['cell_relaxed']) * scale)
        cat = read(champ['relaxed_cif'])
        cat.set_cell(np.array(champ['cell_relaxed']) * scale, scale_atoms=True)
        write(out_dir / 'V0_champion.cif', cat)
        print(f"\n{'='*70}\nrank1 ENSEMBLE ({UMA_MODEL}, n={len(ok)}/{args.n_seeds}) — V0 from EOS BM3 minimum")
        print(f"  ★ V0  = {V0s.mean():.2f} ± {V0s.std():.2f} Å³  "
              f"(median {np.median(V0s):.2f}, range {V0s.min():.2f}–{V0s.max():.2f})")
        print(f"  ★ champion V0 = {cbm['V0_BM']:.2f} Å³ (lowest E0={cbm['E0_BM']:.4f} eV, {champ['rank']})")
        print(f"     V0 cell: a={cp[0]:.4f} b={cp[1]:.4f} c={cp[2]:.4f} Å  "
              f"α={cp[3]:.2f} β={cp[4]:.2f} γ={cp[5]:.2f}°")
        print(f"     saved: {out_dir}/V0_champion.cif")
        print(f"  B0 (bonus, vs LPSCl1.6) = {B0s.mean():.1f} ± {B0s.std():.1f} GPa")
        print("  per-seed (sorted by E0) [E0(eV)  V0(Å³)  B0  B0']:")
        for r in sorted(ok, key=lambda r: r['bm_fit']['E0_BM']):
            b = r['bm_fit']
            print(f"    {r['rank']:16s} {b['E0_BM']:.4f}  {b['V0_BM']:8.2f}  "
                  f"{b['B0_GPa']:6.1f}  {b['B0_prime']:6.2f}")
        print('='*70)
        return

    results['rank1'] = process_rank('rank1', calc, out_dir,
                                    structure=args.rank1_structure, pair_dir=args.rank1_dir)
    if args.rank2_dir or args.rank2_structure:
        results['rank2'] = process_rank('rank2', calc, out_dir,
                                        structure=args.rank2_structure, pair_dir=args.rank2_dir)
    else:
        print("\n[rank2 skipped — no --rank2-dir/--rank2-structure given]")

    # Save full results
    json.dump(results, open(out_dir / 'uma_eos_results.json', 'w'), indent=2, default=str)
    print(f"\n{'='*70}")
    print(f"Full results saved: {out_dir}/uma_eos_results.json")
    print(f"{'='*70}")
    print(f"\nMLIP EOS done — BM3 fit ({UMA_MODEL}):")
    for rk in results:
        bm = results[rk]['bm_fit']
        if bm['fit_success']:
            print(f"  {rk}: V0={bm['V0_BM']:.2f} Å³, B0={bm['B0_GPa']:.1f} GPa, B0'={bm['B0_prime']:.2f}")
        else:
            print(f"  {rk}: BM fit FAILED (check curve)")


if __name__ == '__main__':
    main()
