#!/usr/bin/env python
"""run_cathode_interface.py — Stage 11: NCM-doped-SE adhesion (W_ad).

Wraps the verified production v6 protocol from
`db/inputs/adhesion_templates/adhesion_v6_anneal_test.py` for the
tier_cascade top-K winner loop. Per (winner, baseline):
  - Build 1L NCM (LiNiO2 R-3m hexagonal) of size NCM_NX × NCM_NX × 1
  - Strain winner SE post-anneal cell to NCM xy
  - 5 xy-random shifts (seeds 42-46)
  - Stack SE on NCM with gap 2.5 Å
  - Freeze NCM → 500K Langevin anneal SE 5 ps → quench 100K 2 ps
  - Unfreeze → LBFGS relax (fmax 0.01)
  - Separation: W_ad = (E_sep - E_int) / area × 16.0218 (J/m²)
Compare to LPSCl pristine baselines (comp1, comp3).

Paper claim this enables: "Nd2O3 doping increases NCM-SE adhesion
from X to Y J/m² (relative to pristine LPSCl)" — the user's body of
work (Pustorino/D'Amore/Sundar) ties this to composite cathode
stability.

Usage (from tier_cascade.sh Stage 11):
  python3 tools/doping/run_cathode_interface.py \\
      --ranking $OUT/06_rerank/post_anneal_ranking.json \\
      --anneal_dir $OUT/04_anneal/ \\
      --baselines comp1=db/structures/lpscl_F43m_24G_canonical.cif \\
                  comp3=db/structures/lpscl_F43m_24G_canonical.cif \\
      --out $OUT/11_cathode_interface/ --top 5 --n_seeds 5
"""
import argparse
import json
import sys
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
from _provenance import get_provenance


# v6 protocol constants (verbatim from adhesion_v6_anneal_test.py)
ANNEAL_T = 500
ANNEAL_PS = 5
QUENCH_PS = 2
GAP = 2.5
VACUUM = 30.0
NCM_NX_DEFAULT = 5  # 5x5x1 for Li5.4 family (rhombo); 7 for Li6 cubic


def build_ncm_1L(nx):
    """LiNiO2 R-3m hexagonal, 1 layer slab. From v6 verbatim."""
    from pymatgen.core import Structure, Lattice
    from pymatgen.io.ase import AseAtomsAdaptor
    a, c = 2.878, 14.19
    lat = Lattice.hexagonal(a, c)
    unit = Structure(lat, ["Li", "Ni", "O", "O"],
                     [[0, 0, 0.5], [0, 0, 0],
                      [0, 0, 0.2584], [0, 0, 0.7416]])
    unit.make_supercell([nx, nx, 1])
    atoms = AseAtomsAdaptor().get_atoms(unit)
    pos = atoms.get_positions()
    pos[:, 2] -= pos[:, 2].min()
    atoms.set_positions(pos)
    return atoms


def build_interface(ncm, se, dx, dy):
    """Strain SE to NCM xy, place above NCM with GAP. v6 verbatim."""
    from ase import Atoms
    ncm_cell = ncm.cell.array.copy()
    se_cart = se.get_positions().copy()
    ncm_inv = np.linalg.inv(ncm_cell)
    se_frac = se_cart @ ncm_inv
    se_frac[:, 0] = (se_frac[:, 0] + dx) % 1.0
    se_frac[:, 1] = (se_frac[:, 1] + dy) % 1.0
    se_pos = se_frac @ ncm_cell

    ncm_pos = ncm.get_positions().copy()
    ncm_zmax = ncm_pos[:, 2].max()
    se_zmin = se_pos[:, 2].min()
    se_pos[:, 2] += (ncm_zmax + GAP - se_zmin)
    se_zmax = se_pos[:, 2].max()

    total_z = se_zmax + VACUUM
    combined_cell = ncm_cell.copy()
    combined_cell[2] = [0, 0, total_z]
    symbols = ncm.get_chemical_symbols() + se.get_chemical_symbols()
    positions = np.vstack([ncm_pos, se_pos])
    interface = Atoms(symbols=symbols, positions=positions,
                      cell=combined_cell, pbc=True)
    area = np.linalg.norm(np.cross(ncm_cell[0], ncm_cell[1]))
    return interface, len(ncm), area


def anneal_se(interface, n_ncm, calc_factory):
    """Freeze NCM, anneal SE at 500K, quench. v6 verbatim."""
    from ase.constraints import FixAtoms
    from ase.md.langevin import Langevin
    from ase.md.velocitydistribution import MaxwellBoltzmannDistribution
    from ase import units
    atoms = interface.copy()
    atoms.set_constraint(FixAtoms(indices=list(range(n_ncm))))
    atoms.calc = calc_factory()

    MaxwellBoltzmannDistribution(atoms, temperature_K=ANNEAL_T)
    vel = atoms.get_velocities()
    vel[:n_ncm] = 0.0
    atoms.set_velocities(vel)

    dyn = Langevin(atoms, 1 * units.fs, temperature_K=ANNEAL_T, friction=0.01)
    dyn.run(int(ANNEAL_PS * 1000))

    dyn2 = Langevin(atoms, 1 * units.fs, temperature_K=100, friction=0.05)
    dyn2.run(int(QUENCH_PS * 1000))

    atoms.set_constraint()
    return atoms


def calc_wad(interface, n_ncm, area, calc_factory):
    """Separation method: W_ad in J/m². v6 verbatim."""
    atoms_int = interface.copy()
    atoms_int.calc = calc_factory()
    E_int = atoms_int.get_potential_energy()

    atoms_sep = interface.copy()
    pos = atoms_sep.get_positions()
    pos[n_ncm:, 2] += 30.0
    atoms_sep.set_positions(pos)
    cell = atoms_sep.cell.array.copy()
    cell[2, 2] += 30.0
    atoms_sep.set_cell(cell)
    atoms_sep.calc = calc_factory()
    E_sep = atoms_sep.get_potential_energy()

    Wad = (E_sep - E_int) / area * 16.0218
    return float(Wad), float(E_int), float(E_sep)


def run_one_se(se_atoms, label, ncm_cache, seeds, calc_factory, out_dir):
    """Per-SE (winner or baseline) Wad ensemble. Returns dict."""
    from ase.optimize import LBFGS
    # NCM size choice: rhombo (62-atom) → 5x5, cubic (52-atom) → 7x7
    nx = 5 if len(se_atoms) >= 60 else 7
    if nx not in ncm_cache:
        ncm_cache[nx] = build_ncm_1L(nx)
    ncm = ncm_cache[nx]

    rng = np.random.RandomState(42)
    xy_shifts = [(rng.random(), rng.random()) for _ in range(max(seeds) - 41)]
    wads, per_seed = [], []
    for s in seeds:
        dx, dy = xy_shifts[s - 42]
        t0 = time.time()
        interface, n_ncm, area = build_interface(ncm, se_atoms, dx, dy)
        interface = anneal_se(interface, n_ncm, calc_factory)
        interface.calc = calc_factory()
        try:
            LBFGS(interface, logfile=None).run(fmax=0.01, steps=200)
        except Exception:
            pass
        Wad, E_int, E_sep = calc_wad(interface, n_ncm, area, calc_factory)
        wads.append(Wad)
        per_seed.append({'seed': s, 'dx': float(dx), 'dy': float(dy),
                         'Wad_J_m2': Wad, 'E_int_eV': E_int,
                         'E_sep_eV': E_sep, 'elapsed_s': time.time() - t0})
        print(f"      [{label} seed={s}] Wad={Wad:+.3f} "
              f"({dx:.2f},{dy:.2f}) {time.time()-t0:.0f}s", flush=True)

    return {
        'label': label,
        'ncm_nx': nx,
        'Wad_mean_J_m2': float(np.mean(wads)),
        'Wad_std_J_m2': float(np.std(wads)),
        'n_seeds': len(wads),
        'per_seed': per_seed,
    }


def main():
    p = argparse.ArgumentParser(description=__doc__,
                               formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('--ranking', required=True)
    p.add_argument('--anneal_dir', required=True)
    p.add_argument('--baselines', nargs='+', default=[],
                   help='Baseline SEs as label=path/to/cif (multiple). '
                        'Run alongside winners for Δ_Wad reference.')
    p.add_argument('--out', required=True)
    p.add_argument('--top', type=int, default=5)
    p.add_argument('--n_seeds', type=int, default=5,
                   help='xy-shift seeds per (SE, NCM). v6 default 5.')
    p.add_argument('--device', default='cuda')
    args = p.parse_args()

    from ase.io import read
    from fairchem.core import pretrained_mlip, FAIRChemCalculator

    predictor = pretrained_mlip.get_predict_unit("uma-s-1p1", device=args.device)

    def calc_factory():
        return FAIRChemCalculator(predictor, task_name="omat")

    ranking = json.loads(Path(args.ranking).read_text())
    winners = ranking.get('ranked_by_post_anneal', [])[:args.top]
    if not winners:
        raise SystemExit(f"No winners in {args.ranking}")

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    seeds = list(range(42, 42 + args.n_seeds))
    ncm_cache = {}

    print(f"\n=== Stage 11 NCM-SE adhesion v6 — top-{args.top} winners "
          f"+ {len(args.baselines)} baselines ===")
    print(f"  Protocol: NCM frozen → 500K SE anneal {ANNEAL_PS}ps → "
          f"quench 100K {QUENCH_PS}ps → LBFGS")
    print(f"  Seeds per SE: {seeds}\n")

    all_results = {'winners': [], 'baselines': []}

    # Baselines first (cached NCM speeds up subsequent winner runs)
    for spec in args.baselines:
        if '=' not in spec:
            print(f"  ⚠ skip malformed baseline spec: {spec}")
            continue
        label, path = spec.split('=', 1)
        if not Path(path).exists():
            print(f"  ⚠ skip baseline {label}: {path} missing")
            continue
        print(f"  Baseline {label} — loading {path}")
        se = read(path)
        try:
            res = run_one_se(se, label, ncm_cache, seeds, calc_factory,
                             out / 'baselines')
        except Exception as e:
            print(f"    ERROR {e}")
            res = {'label': label, 'error': str(e)}
        all_results['baselines'].append(res)
        (out / f'baseline_{label}.json').write_text(
            json.dumps(res, indent=2, default=str))

    # Winners
    for i, rec in enumerate(winners, 1):
        name = rec['name']
        xyz = Path(args.anneal_dir) / name / 'post_relax.xyz'
        if not xyz.exists():
            print(f"  [{i}/{len(winners)}] {name}: MISSING {xyz} — skip")
            continue
        print(f"  [{i}/{len(winners)}] {name}")
        se = read(str(xyz))
        try:
            res = run_one_se(se, name, ncm_cache, seeds, calc_factory,
                             out / name)
        except Exception as e:
            print(f"    ERROR {e}")
            res = {'label': name, 'error': str(e)}
        res['dopant'] = rec.get('dopant')
        res['site'] = rec.get('site')
        res['anion_site_label'] = rec.get('anion_site_label')
        all_results['winners'].append(res)
        (out / name / 'wad.json').write_text(
            json.dumps(res, indent=2, default=str))

    # Aggregate
    summary = {
        'provenance': get_provenance(),
        'protocol': 'v6 (1L NCM, NCM-frozen 500K SE anneal, separation Wad)',
        'config': {'top': args.top, 'n_seeds': args.n_seeds,
                   'anneal_T_K': ANNEAL_T, 'anneal_ps': ANNEAL_PS,
                   'quench_ps': QUENCH_PS, 'gap_A': GAP},
        'baselines': all_results['baselines'],
        'winners': all_results['winners'],
    }

    # Δ_Wad reporting (winner vs each baseline)
    print(f"\n=== Wad summary (J/m²) — mean ± std (n_seeds={args.n_seeds}) ===")
    baseline_lookup = {b.get('label'): b for b in all_results['baselines']
                       if 'Wad_mean_J_m2' in b}
    header = f"  {'Winner / Baseline':<40}{'Wad':>8}{'σ_Wad':>8}"
    for b_label in baseline_lookup:
        header += f"{'Δ vs '+b_label:>14}"
    print(header)
    for b in all_results['baselines']:
        if 'Wad_mean_J_m2' not in b:
            continue
        print(f"  baseline {b['label']:<31}"
              f"{b['Wad_mean_J_m2']:>+8.3f}{b['Wad_std_J_m2']:>8.3f}")
    for w in all_results['winners']:
        if 'Wad_mean_J_m2' not in w:
            continue
        row = (f"  {w['label'][:38]:<40}"
               f"{w['Wad_mean_J_m2']:>+8.3f}{w['Wad_std_J_m2']:>8.3f}")
        for b_label, b in baseline_lookup.items():
            delta = w['Wad_mean_J_m2'] - b['Wad_mean_J_m2']
            row += f"{delta:>+13.3f}"
        print(row)

    (out / 'cathode_interface_summary.json').write_text(
        json.dumps(summary, indent=2, default=str))
    print(f"\n✓ Stage 11 → {out}/cathode_interface_summary.json")


if __name__ == '__main__':
    main()
