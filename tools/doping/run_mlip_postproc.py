#!/usr/bin/env python
"""run_mlip_postproc.py — full MLIP post-processing per structure.

For each input xyz, runs in order:
  1. Light anneal (300 K, 20 ps, optional). NOTE: 300K @ 20ps is mostly
     finite-T noise injection rather than true Li-sublattice annealing
     (Arrhenius rate × 20ps ≈ 0.01 hop/Li at 300K). Use temperature=500
     and time_ps=50 for actual Pipeline-Step-3 anneal (kT=0.043 eV
     vs Li hop Eₐ=0.2 eV barrier).
  2. EOS volume sweep (94-106% in 7 steps: 0.94/0.96/0.98/1.00/1.02/
     1.04/1.06), Birch-Murnaghan 3rd-order fit
     → V0, B0, B0', R² (returns None for B0/V0 if r²<0.95 — A-3 fix)
  3. Elastic constants via finite strain (6 Voigt strains, ε = ±0.005),
     Voigt-Reuss-Hill average → B, G, E (Young), ν (Poisson), G/B (Pugh).
     Sign convention: ASE atoms.get_stress() returns positive stress
     for compression (= negative of dE/dV/V), so dσ/dε > 0 → C_ii > 0.

All UMA, no extra DFT. Output: per-structure JSON + global summary.

Usage:
  python3 tools/doping/run_mlip_postproc.py \\
      --winners runs/.../winners.json \\
      --out runs/.../mlip_postproc/ \\
      --device cuda

  # Skip steps (per-step toggle)
  python3 ... --no_anneal --no_elastic   # only EOS

  # Specific xyz instead of winners JSON
  python3 ... --xyz path/a.xyz path/b.xyz --out ...
"""
import argparse
import json
import sys
import time
from pathlib import Path
import numpy as np
from ase.io import read, write
from ase.optimize import FIRE
from ase.md.langevin import Langevin
from ase.md.velocitydistribution import MaxwellBoltzmannDistribution
from ase import units

try:
    from ase.filters import FrechetCellFilter as CellFilter
except ImportError:
    try:
        from ase.constraints import ExpCellFilter as CellFilter
    except ImportError:
        from ase.constraints import UnitCellFilter as CellFilter

sys.path.insert(0, str(Path(__file__).parent))
from _provenance import get_provenance


def load_uma(device='cuda', task='omat'):
    from fairchem.core import pretrained_mlip, FAIRChemCalculator
    predictor = pretrained_mlip.get_predict_unit('uma-s-1p1', device=device)
    return FAIRChemCalculator(predictor, task_name=task)


def light_anneal(atoms, T=300, time_ps=20, dt_fs=2.0, relax_steps=500,
                fmax=0.05):
    """Brief Langevin NVT then cell+positions relax. Returns relaxed atoms +
    log dict."""
    MaxwellBoltzmannDistribution(atoms, temperature_K=T)
    n_steps = int(time_ps * 1000 / dt_fs)
    dyn = Langevin(atoms, dt_fs * units.fs, temperature_K=T, friction=0.01,
                  logfile=None)
    t0 = time.time()
    dyn.run(n_steps)
    t_md = time.time() - t0
    opt = FIRE(CellFilter(atoms), logfile=None)
    t1 = time.time()
    opt.run(fmax=fmax, steps=relax_steps)
    t_relax = time.time() - t1
    return atoms, {'T_K': T, 'time_ps': time_ps,
                   'n_relax_steps': opt.get_number_of_steps(),
                   'converged': opt.get_number_of_steps() < relax_steps,
                   't_md_s': t_md, 't_relax_s': t_relax,
                   'E_post_atom': atoms.get_potential_energy() / len(atoms)}


def eos_sweep(atoms_ref, calc, fractions=(0.94, 0.96, 0.98, 1.00, 1.02, 1.04, 1.06),
             fmax=0.05, relax_steps=500):
    """Volume sweep + Birch-Murnaghan 3rd-order fit. atoms_ref is the
    relaxed reference at V0; we scale its lattice by f^(1/3) per point."""
    V = []
    E = []
    n = len(atoms_ref)
    for f in fractions:
        atoms = atoms_ref.copy()
        new_cell = atoms.cell.array * f ** (1/3)
        atoms.set_cell(new_cell, scale_atoms=True)
        atoms.calc = calc
        # Atoms-only relax (cell fixed for EOS)
        opt = FIRE(atoms, logfile=None)
        opt.run(fmax=fmax, steps=relax_steps)
        V.append(atoms.get_volume())
        E.append(atoms.get_potential_energy())
    V = np.array(V)
    E = np.array(E)
    # 3rd-order Birch-Murnaghan fit
    try:
        from scipy.optimize import curve_fit
        def bm3(V, E0, V0, B0, Bp):
            eta = (V0 / V) ** (2/3)
            return (E0 + (9 * V0 * B0 / 16) *
                    ((eta - 1) ** 3 * Bp + (eta - 1) ** 2 * (6 - 4 * eta)))
        p0 = [E.min(), V[E.argmin()], 0.1, 4.0]  # B0 in eV/Å³ ≈ 0.1 = 16 GPa
        popt, _ = curve_fit(bm3, V, E, p0=p0, maxfev=10000)
        E0, V0, B0, Bp = popt
        # B0 in GPa: 1 eV/Å³ = 160.218 GPa
        B0_GPa = B0 * 160.21766208
        # R²
        E_pred = bm3(V, *popt)
        ss_res = np.sum((E - E_pred) ** 2)
        ss_tot = np.sum((E - E.mean()) ** 2)
        r2 = 1 - ss_res / ss_tot if ss_tot > 0 else 0
        # A-3 fix: r² gate. Diverged BM3 fits (r²<0.95) shouldn't poison
        # downstream rankings; flag B0_GPa as None and set fit_quality_ok=False
        # so combine_rankings can drop them.
        fit_ok = r2 >= 0.95 and 0 < V0 < 5 * V[len(V)//2]
        return {'V_points': V.tolist(), 'E_points': E.tolist(),
                'fractions': list(fractions),
                'V0': float(V0) if fit_ok else None,
                'V0_per_atom': float(V0) / n if fit_ok else None,
                'E0': float(E0) if fit_ok else None,
                'B0_eV_per_A3': float(B0) if fit_ok else None,
                'B0_GPa': float(B0_GPa) if fit_ok else None,
                'Bp': float(Bp) if fit_ok else None,
                'r2': float(r2),
                'fit_quality_ok': fit_ok,
                'fit_quality_reason': ('OK' if fit_ok
                                      else f'r²={r2:.4f} < 0.95 or V0 unphysical')}
    except Exception as e:
        return {'V_points': V.tolist(), 'E_points': E.tolist(),
                'fractions': list(fractions),
                'fit_error': str(e)}


def elastic_finite_strain(atoms_ref, calc, eps=0.005, fmax=0.05,
                          relax_steps=300):
    """6 independent Voigt strains × ±eps. Compute stress → Cij.
    Voigt-Reuss-Hill avg → B, G, E, ν, G/B.
    """
    # Strain matrices for ε₁..ε₆ (Voigt convention)
    voigt = [
        np.array([[1, 0, 0], [0, 0, 0], [0, 0, 0]]),  # ε₁ = εxx
        np.array([[0, 0, 0], [0, 1, 0], [0, 0, 0]]),  # ε₂ = εyy
        np.array([[0, 0, 0], [0, 0, 0], [0, 0, 1]]),  # ε₃ = εzz
        np.array([[0, 0, 0], [0, 0, 0.5], [0, 0.5, 0]]),  # ε₄ = εyz
        np.array([[0, 0, 0.5], [0, 0, 0], [0.5, 0, 0]]),  # ε₅ = εxz
        np.array([[0, 0.5, 0], [0.5, 0, 0], [0, 0, 0]]),  # ε₆ = εxy
    ]

    cell0 = atoms_ref.cell.array.copy()
    n = len(atoms_ref)
    Cij = np.zeros((6, 6))
    for i, strain in enumerate(voigt):
        stresses_pos_neg = []
        for sign in (+1, -1):
            atoms = atoms_ref.copy()
            F = np.eye(3) + sign * eps * strain
            atoms.set_cell(cell0 @ F, scale_atoms=True)
            atoms.calc = calc
            opt = FIRE(atoms, logfile=None)
            opt.run(fmax=fmax, steps=relax_steps)
            # Stress in Voigt order: [σxx, σyy, σzz, σyz, σxz, σxy] (ASE convention)
            stresses_pos_neg.append(atoms.get_stress(voigt=True))
        sigma_pos, sigma_neg = stresses_pos_neg
        # Central difference: ∂σ/∂ε
        dsigma_de = (sigma_pos - sigma_neg) / (2 * eps)
        Cij[:, i] = dsigma_de  # column i = ∂σⱼ/∂εᵢ

    # Symmetrize
    Cij = 0.5 * (Cij + Cij.T)
    # ASE stress is in eV/Å³; convert to GPa
    Cij_GPa = Cij * 160.21766208

    # Voigt-Reuss-Hill
    C = Cij_GPa
    Bv = (C[0, 0] + C[1, 1] + C[2, 2] + 2 * (C[0, 1] + C[0, 2] + C[1, 2])) / 9
    Gv = ((C[0, 0] + C[1, 1] + C[2, 2]) - (C[0, 1] + C[0, 2] + C[1, 2])
          + 3 * (C[3, 3] + C[4, 4] + C[5, 5])) / 15
    try:
        S = np.linalg.inv(C)
        Br = 1 / (S[0, 0] + S[1, 1] + S[2, 2] + 2 * (S[0, 1] + S[0, 2] + S[1, 2]))
        Gr = 15 / (4 * (S[0, 0] + S[1, 1] + S[2, 2])
                  - 4 * (S[0, 1] + S[0, 2] + S[1, 2])
                  + 3 * (S[3, 3] + S[4, 4] + S[5, 5]))
    except np.linalg.LinAlgError:
        Br = Gr = None

    Bh = (Bv + Br) / 2 if Br is not None else Bv
    Gh = (Gv + Gr) / 2 if Gr is not None else Gv
    if Bh and Gh:
        E_young = 9 * Bh * Gh / (3 * Bh + Gh)
        nu = (3 * Bh - 2 * Gh) / (2 * (3 * Bh + Gh))
        pugh = Gh / Bh
    else:
        E_young = nu = pugh = None

    return {
        'eps': eps,
        'Cij_GPa': Cij_GPa.tolist(),
        'B_voigt_GPa': float(Bv), 'B_reuss_GPa': float(Br) if Br else None,
        'B_hill_GPa': float(Bh),
        'G_voigt_GPa': float(Gv), 'G_reuss_GPa': float(Gr) if Gr else None,
        'G_hill_GPa': float(Gh),
        'E_young_GPa': float(E_young) if E_young else None,
        'poisson_nu': float(nu) if nu else None,
        'pugh_ratio_GoverB': float(pugh) if pugh else None,
    }


def process_one(xyz_path, calc, out_dir, args):
    name = xyz_path.stem
    work = out_dir / name
    work.mkdir(parents=True, exist_ok=True)

    atoms = read(str(xyz_path))
    atoms.calc = calc
    record = {'name': name, 'xyz_input': str(xyz_path),
              'n_atoms': len(atoms),
              'composition': {el: int(c) for el, c in
                              zip(*np.unique(atoms.get_chemical_symbols(),
                                            return_counts=True))}}

    # 0. Refresh relax to ensure starting at minimum
    opt = FIRE(CellFilter(atoms), logfile=None)
    opt.run(fmax=0.05, steps=500)
    record['E_pre_anneal_per_atom'] = atoms.get_potential_energy() / len(atoms)

    # 1. Anneal (optional)
    if not args.no_anneal:
        atoms, log = light_anneal(atoms, T=args.anneal_T,
                                 time_ps=args.anneal_ps,
                                 relax_steps=args.relax_steps)
        record['anneal'] = log
    record['E_post_anneal_per_atom'] = atoms.get_potential_energy() / len(atoms)
    write(work / 'post_anneal.xyz', atoms)

    # 2. EOS
    if not args.no_eos:
        t0 = time.time()
        record['eos'] = eos_sweep(atoms, calc,
                                  fractions=tuple(args.eos_fractions),
                                  fmax=args.eos_fmax,
                                  relax_steps=args.relax_steps)
        record['eos']['t_s'] = time.time() - t0

    # 3. Elastic
    if not args.no_elastic:
        t0 = time.time()
        record['elastic'] = elastic_finite_strain(atoms, calc,
                                                  eps=args.elastic_eps,
                                                  fmax=args.elastic_fmax,
                                                  relax_steps=args.relax_steps)
        record['elastic']['t_s'] = time.time() - t0

    (work / 'postproc.json').write_text(json.dumps(record, indent=2, default=str))
    return record


def main():
    p = argparse.ArgumentParser(description=__doc__,
                               formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('--winners', help='winners.json from select_winners.py')
    p.add_argument('--xyz', nargs='+', help='specific xyz files')
    p.add_argument('--out', required=True)
    p.add_argument('--device', default='cuda')
    p.add_argument('--task', default='omat')
    # Step toggles
    p.add_argument('--no_anneal', action='store_true')
    p.add_argument('--no_eos', action='store_true')
    p.add_argument('--no_elastic', action='store_true')
    # Anneal params
    p.add_argument('--anneal_T', type=float, default=300,
                  help='Light anneal T (default 300K)')
    p.add_argument('--anneal_ps', type=float, default=20,
                  help='Light anneal time (default 20 ps)')
    # EOS params
    p.add_argument('--eos_fractions', nargs='+', type=float,
                  default=[0.94, 0.96, 0.98, 1.00, 1.02, 1.04, 1.06])
    p.add_argument('--eos_fmax', type=float, default=0.05)
    # Elastic params
    p.add_argument('--elastic_eps', type=float, default=0.005,
                  help='Voigt strain magnitude')
    p.add_argument('--elastic_fmax', type=float, default=0.05)
    # General
    p.add_argument('--relax_steps', type=int, default=500)
    p.add_argument('--limit', type=int, default=None,
                  help='Limit to first N structures (debug)')
    args = p.parse_args()

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    if args.winners:
        winners = json.loads(Path(args.winners).read_text())['winners']
        xyz_paths = [Path(w['xyz_file']) for w in winners
                    if Path(w.get('xyz_file', '')).exists()]
    elif args.xyz:
        xyz_paths = [Path(p) for p in args.xyz]
    else:
        p.error("Provide --winners or --xyz")

    if args.limit:
        xyz_paths = xyz_paths[:args.limit]

    # Resume
    summary_path = out / 'postproc_summary.json'
    done = {}
    if summary_path.exists():
        existing = json.loads(summary_path.read_text())
        done = {r['name']: r for r in existing.get('records', [])}
        print(f"Resume: {len(done)} already done")
    todo = [p for p in xyz_paths if p.stem not in done]
    print(f"To process: {len(todo)}/{len(xyz_paths)}")

    print(f"Loading UMA-s-1p1 ({args.device})...")
    calc = load_uma(args.device, args.task)

    records = list(done.values())
    t_start = time.time()
    for i, xpath in enumerate(todo):
        print(f"\n[{i+1}/{len(todo)}] {xpath.stem}")
        try:
            rec = process_one(xpath, calc, out, args)
            records.append(rec)
            ann = rec.get('anneal', {})
            eos = rec.get('eos', {})
            ela = rec.get('elastic', {})
            print(f"  E={rec.get('E_post_anneal_per_atom', float('nan')):.4f} "
                  f"B0={eos.get('B0_GPa', float('nan')):.1f} GPa "
                  f"E_young={ela.get('E_young_GPa', float('nan')):.1f} GPa "
                  f"Pugh={ela.get('pugh_ratio_GoverB', float('nan')):.2f}")
        except Exception as e:
            print(f"  ❌ FAILED: {e}")
            records.append({'name': xpath.stem, 'error': str(e)})
        # Periodic save
        if (i + 1) % 3 == 0 or (i + 1) == len(todo):
            summary_path.write_text(json.dumps({
                'provenance': get_provenance(),
                'cli_args': vars(args),
                'n_done': len(records),
                'records': records,
            }, indent=2, default=str))

    print(f"\n{'='*60}")
    print(f"✓ Post-proc done: {len(records)} structures, "
          f"{time.time()-t_start:.0f}s")
    print(f"✓ Summary: {summary_path}")


if __name__ == '__main__':
    main()
