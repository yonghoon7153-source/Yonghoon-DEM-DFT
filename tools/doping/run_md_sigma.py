#!/usr/bin/env python
"""run_md_sigma.py — Stage 10: MLIP-MD ionic conductivity (σ_Li).

Ports the verified production md_lpscl_v2.py (gabia
/data/work/v30u_ensemble/, uploaded 2026-03-09 by user) onto the
tier_cascade top-K winner loop. Per winner: 2×2×2 supercell × 3T MD ×
50 ps production → MSD → Einstein D → Nernst-Einstein σ →
Arrhenius → 300K extrapolation.

This is the paper-essential σ_Li axis that BVSE proxy
(migration_volume_fraction) cannot give. The pipeline previously
predicted "Li mobility" qualitatively; this stage produces the
absolute σ_300K number the paper claims.

Important caveats (also printed at runtime):
  - Haven ratio H_R not applied. Real σ ≈ H_R × σ_NE (H_R ≈ 0.3-0.7
    for argyrodites). Conservative reporting: divide by 2 for upper bound.
  - 50 ps × 3T per winner is a *screening-grade* number. Production
    needs 100-200 ps + more T points (Arrhenius R² guard).
  - UMA-s-1p2 sulfide PES has known softening (Wang 2025); cross-check
    against KISTI AIMD for at least one winner before paper claim.

Usage (from tier_cascade.sh Stage 10):
  python3 tools/doping/run_md_sigma.py \\
      --ranking $OUT/06_rerank/post_anneal_ranking.json \\
      --anneal_dir $OUT/04_anneal/ \\
      --out $OUT/10_md_sigma/ \\
      --top 5 \\
      --temps 600 800 1000 \\
      --prod_ps 50
"""
import argparse
import json
import sys
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
from _provenance import get_provenance


def run_one_winner(xyz_path: Path, out_dir: Path, temps, equil_ps,
                   prod_ps, dt_fs, save_every, supercell, device):
    """Returns per-winner σ_md dict. Adapted from md_lpscl_v2.py."""
    from ase.io import read, write
    from ase.build import make_supercell
    from ase.md.langevin import Langevin
    from ase.md.velocitydistribution import MaxwellBoltzmannDistribution
    from ase import units
    from fairchem.core import pretrained_mlip, FAIRChemCalculator
    from scipy.stats import linregress

    atoms_prim = read(str(xyz_path))
    sup = supercell * np.eye(3, dtype=int)
    atoms_base = make_supercell(atoms_prim, sup)
    n_total = len(atoms_base)
    n_Li = sum(1 for s in atoms_base.get_chemical_symbols() if s == 'Li')
    if n_Li == 0:
        return {'error': 'no Li atoms after supercell build',
                'n_total': n_total}

    print(f"    prim {len(atoms_prim)} → {supercell}x supercell {n_total} atoms "
          f"({n_Li} Li)", flush=True)

    predictor = pretrained_mlip.get_predict_unit("uma-s-1p1", device=device)
    calc = FAIRChemCalculator(predictor, task_name="omat")

    equil_steps = int(equil_ps * 1000 / dt_fs)
    prod_steps = int(prod_ps * 1000 / dt_fs)
    results = {}

    for T in temps:
        t0 = time.time()
        atoms = atoms_base.copy()
        atoms.calc = calc

        MaxwellBoltzmannDistribution(atoms, temperature_K=T)
        md = Langevin(atoms, timestep=dt_fs * units.fs,
                      temperature_K=T, friction=0.01 / units.fs)

        # Equilibration
        md.run(equil_steps)

        # Production + PBC unwrapping. v4.5.1 M-C fix: use full 3x3 cell
        # matrix (triclinic-safe). Previous version used only diagonal of
        # cell — correct for cubic prim cells but biased for doped
        # configurations whose post-anneal cell drifts toward monoclinic
        # (β ≈ 90 ± 1°). Also log cell parameters as sanity check.
        symbols = atoms.get_chemical_symbols()
        li_idx = [i for i, s in enumerate(symbols) if s == 'Li']
        cell_matrix = np.array(atoms.get_cell())
        inv_cell = np.linalg.inv(cell_matrix)
        cellpar = atoms.cell.cellpar()
        print(f"      cell a={cellpar[0]:.3f} b={cellpar[1]:.3f} "
              f"c={cellpar[2]:.3f}  α={cellpar[3]:.2f} "
              f"β={cellpar[4]:.2f} γ={cellpar[5]:.2f}", flush=True)

        prev_pos = atoms.get_positions()[li_idx]
        unwrapped = prev_pos.copy()
        all_unwrapped = [unwrapped.copy()]

        for step in range(prod_steps):
            md.run(1)
            cur_pos = atoms.get_positions()[li_idx]
            # Triclinic-safe minimum-image: project diff into fractional,
            # subtract nearest integer image, project back.
            frac_diff = (cur_pos - prev_pos) @ inv_cell
            frac_diff -= np.round(frac_diff)
            diff = frac_diff @ cell_matrix
            unwrapped = unwrapped + diff
            prev_pos = cur_pos.copy()
            if step % save_every == 0:
                all_unwrapped.append(unwrapped.copy())

        all_unwrapped = np.array(all_unwrapped)
        n_frames = len(all_unwrapped)
        msd = np.mean(np.sum((all_unwrapped - all_unwrapped[0])**2,
                             axis=2), axis=1)
        dt_arr = np.arange(n_frames) * save_every * dt_fs * 1e-15

        fit_start = n_frames // 2
        slope, intercept, r, _, _ = linregress(dt_arr[fit_start:],
                                                msd[fit_start:])
        D_cm2s = slope / 6 * 1e-16

        vol_cm3 = atoms.get_volume() * 1e-24
        n_density = n_Li / vol_cm3
        kB = 1.380649e-23
        q = 1.602176634e-19
        sigma = (n_density * 1e6) * q**2 * (D_cm2s * 1e-4) / (kB * T) * 1e-2

        elapsed = time.time() - t0
        # v4.5.1 M-D fix: flag low-R² points so Arrhenius fit can exclude
        # them. 600K with 50 ps is marginal (≈0.5 Li hop / atom) — R²
        # often < 0.85 even though higher T is fine. Without this flag
        # a noisy low-T point biases Ea / D_300K extrapolation.
        reliable = bool(r**2 >= 0.85)
        results[T] = {'D_cm2s': D_cm2s, 'sigma_S_cm': sigma,
                      'msd_R2': r**2, 'reliable': reliable,
                      'elapsed_min': elapsed / 60.0}
        flag = '' if reliable else '  ⚠ low R² (Arrhenius excludes)'
        print(f"      T={T}K  D={D_cm2s:.3e}  σ={sigma:.3e} S/cm  "
              f"R²={r**2:.3f}  ({elapsed/60:.1f}min){flag}", flush=True)

        # Save raw MSD for paper SI reproducibility
        np.savetxt(out_dir / f"msd_{T}K.dat",
                   np.column_stack([dt_arr * 1e12, msd]),
                   header=f"time(ps)  MSD(A^2)  T={T}K  D={D_cm2s:.3e}")

    # Arrhenius — needs ≥ 3 reliable T points (v4.5.1 M-D fix).
    # Exclude T points with MSD R² < 0.85 (low-T noisy fit). If fewer
    # than 3 reliable points, fall back to all available T but flag
    # the result as low-confidence so the user knows to extend prod_ps
    # or add T points.
    reliable_Ts = sorted(T for T in results if results[T].get('reliable'))
    fit_Ts = reliable_Ts if len(reliable_Ts) >= 3 else sorted(results.keys())
    fit_quality = ('reliable' if len(reliable_Ts) >= 3
                   else f'low-confidence (only {len(reliable_Ts)}/{len(results)} '
                        f'T with R²≥0.85, fell back to all)')
    if len(fit_Ts) < 3:
        return {'per_temperature': results,
                'warning': f'Arrhenius needs ≥3 T points, have {len(fit_Ts)}',
                'fit_quality': fit_quality}

    Ts = np.array(fit_Ts, dtype=float)
    Ds = np.array([results[T]['D_cm2s'] for T in fit_Ts])
    inv_T_1000 = 1000.0 / Ts
    ln_D = np.log(Ds)
    slope_arr, intercept_arr, r_arr, _, _ = linregress(inv_T_1000, ln_D)
    Ea_eV = -slope_arr * 8.617333e-5 * 1000

    D_300K = float(np.exp(intercept_arr + slope_arr * (1000.0 / 300)))
    kB = 1.380649e-23
    q = 1.602176634e-19
    vol_cm3 = atoms.get_volume() * 1e-24
    n_density = n_Li / vol_cm3
    sigma_300K = (n_density * 1e6) * q**2 * (D_300K * 1e-4) / (kB * 300) * 1e-2

    return {
        'per_temperature': results,
        'arrhenius': {
            'Ea_eV': float(Ea_eV),
            'D_300K_cm2s': D_300K,
            'sigma_300K_S_cm_NE': float(sigma_300K),
            'sigma_300K_S_cm_with_HR_0p5_estimate': float(sigma_300K * 0.5),
            'fit_R2': float(r_arr**2),
            'n_T_points_used': len(Ts),
            'n_T_points_total': len(results),
            'T_points_used_K': fit_Ts,
            'fit_quality': fit_quality,
        },
        'n_Li': int(n_Li),
        'n_atoms': int(n_total),
        'supercell': supercell,
        'caveats': [
            'Haven ratio not applied — divide σ_NE by ~2 for argyrodite '
            'literature consistency (HR ≈ 0.3-0.7).',
            'UMA-s-1p2 sulfide PES softening (Wang 2025) — verify against '
            'AIMD for at least one winner.',
            f'Production {prod_ps} ps screening-grade only.',
        ],
    }


def main():
    p = argparse.ArgumentParser(description=__doc__,
                               formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('--ranking', required=True,
                   help='06_rerank/post_anneal_ranking.json')
    p.add_argument('--anneal_dir', required=True,
                   help='04_anneal/ — each winner has post_relax.xyz here')
    p.add_argument('--out', required=True)
    p.add_argument('--top', type=int, default=5)
    p.add_argument('--temps', type=int, nargs='+', default=[600, 800, 1000])
    p.add_argument('--equil_ps', type=float, default=10.0)
    p.add_argument('--prod_ps', type=float, default=50.0)
    p.add_argument('--dt_fs', type=float, default=2.0)
    p.add_argument('--save_every', type=int, default=20)
    p.add_argument('--supercell', type=int, default=2,
                   help='Supercell multiplier (default 2 → 2x2x2). Set 1 '
                        'for very large primitive cells.')
    p.add_argument('--device', default='cuda')
    args = p.parse_args()

    ranking = json.loads(Path(args.ranking).read_text())
    records = ranking.get('ranked_by_post_anneal', [])[:args.top]
    if not records:
        raise SystemExit(f"No records in {args.ranking}")

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    print(f"\n=== Stage 10 σ_Li MD — top-{args.top} winners ===")
    print(f"  T grid: {args.temps} K")
    print(f"  Per (T, winner): {args.equil_ps} ps equil + {args.prod_ps} ps prod")
    print(f"  Supercell: {args.supercell}×{args.supercell}×{args.supercell}")
    print(f"  ⚠ Haven ratio NOT applied — divide σ by ~2 for argyrodite "
          f"comparison.\n")

    all_results = {}
    for i, rec in enumerate(records, 1):
        name = rec['name']
        winner_dir = Path(args.anneal_dir) / name
        xyz = winner_dir / 'post_relax.xyz'
        if not xyz.exists():
            print(f"  [{i}/{len(records)}] {name}: MISSING {xyz} — skip")
            continue

        print(f"  [{i}/{len(records)}] {name}")
        per_winner_out = out / name
        per_winner_out.mkdir(parents=True, exist_ok=True)
        try:
            res = run_one_winner(xyz, per_winner_out, args.temps,
                                 args.equil_ps, args.prod_ps, args.dt_fs,
                                 args.save_every, args.supercell, args.device)
        except Exception as e:
            print(f"    ERROR {e}")
            res = {'error': str(e)}

        res['name'] = name
        res['dopant'] = rec.get('dopant')
        res['site'] = rec.get('site')
        res['anion_site_label'] = rec.get('anion_site_label')
        (per_winner_out / 'sigma_md.json').write_text(
            json.dumps(res, indent=2, default=str))
        all_results[name] = res

    summary = {
        'provenance': get_provenance(),
        'config': {
            'top': args.top, 'temps_K': args.temps,
            'equil_ps': args.equil_ps, 'prod_ps': args.prod_ps,
            'dt_fs': args.dt_fs, 'supercell': args.supercell,
        },
        'records': list(all_results.values()),
    }
    (out / 'sigma_md_summary.json').write_text(
        json.dumps(summary, indent=2, default=str))

    print(f"\n=== Summary (Nernst-Einstein, no H_R correction) ===")
    print(f"{'Winner':<40}{'Ea(eV)':>10}{'D_300K':>14}{'σ_300K(S/cm)':>16}")
    for r in summary['records']:
        arr = r.get('arrhenius')
        if not arr:
            print(f"  {r['name'][:38]:<40}  (incomplete)")
            continue
        print(f"  {r['name'][:38]:<40}"
              f"{arr['Ea_eV']:>9.3f}"
              f"{arr['D_300K_cm2s']:>13.2e}"
              f"{arr['sigma_300K_S_cm_NE']:>15.2e}")
    print(f"\n✓ Stage 10 → {out}/sigma_md_summary.json")


if __name__ == '__main__':
    main()
