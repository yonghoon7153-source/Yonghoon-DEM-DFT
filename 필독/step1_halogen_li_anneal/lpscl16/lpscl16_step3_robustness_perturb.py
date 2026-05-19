"""
lpscl16 Step 3 — robustness check via random Li perturbation.

Protocol mirrors Nd-doped phase_2_5_quality_check (db/compositions/modelc_nd_doped.json):
  - Load champion xyz (from step1 or step2 winner)
  - 20 trials: perturb Li positions randomly (max |dr|=0.5 Å, uniform)
  - UMA FIRE relax each (fmax 0.005, max 300 steps)
  - Compare relaxed E to champion E
  - PASS if all 20 trials yield E ≥ E_champion (within MLIP precision ~10 meV)

If any trial < E_champion: that's a deeper basin → re-run Step 2 anneal on it.

Reads:  lpscl16_champion.xyz (written by step2)
Writes: lpscl16_robustness.json (per-trial E + verdict)

Reference: kb/methodology/argyrodite_mechanical_pipeline_v2.md (gap-filling for
modelC v2: Nd-doped had robustness check, pristine modelC did not).
"""
import argparse
import json
import numpy as np
from ase.io import read, write
from ase.optimize import FIRE
from fairchem.core import pretrained_mlip
from fairchem.core.calculate.ase_calculator import FAIRChemCalculator

def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument('--champion', default='lpscl16_champion.xyz',
                   help='champion structure xyz (from step1/step2 winner)')
    p.add_argument('--n_trials', type=int, default=20)
    p.add_argument('--perturb_A', type=float, default=0.5,
                   help='max Li displacement, Å (uniform random)')
    p.add_argument('--seed', type=int, default=42)
    p.add_argument('--fmax', type=float, default=0.005)
    p.add_argument('--max_steps', type=int, default=300)
    p.add_argument('--out_json', default='lpscl16_robustness.json')
    return p.parse_args()

def main():
    args = parse_args()
    predictor = pretrained_mlip.get_predict_unit("uma-s-1p1", device="cuda")

    def relax(atoms):
        atoms.calc = FAIRChemCalculator(predictor, task_name="omat")
        try: FIRE(atoms, logfile=None).run(fmax=args.fmax, steps=args.max_steps)
        except Exception: pass
        return atoms.get_potential_energy()

    champion = read(args.champion)
    E_champion = relax(champion.copy())
    print(f"Champion: {args.champion}")
    print(f"E_champion (re-relaxed): {E_champion:.4f} eV")
    print(f"n_trials={args.n_trials}, perturb_A={args.perturb_A}, seed={args.seed}")
    print("=" * 60)

    rng = np.random.RandomState(args.seed)
    li_idx = [i for i, s in enumerate(champion.get_chemical_symbols()) if s == 'Li']

    results = []
    for t in range(args.n_trials):
        a = champion.copy()
        pos = a.get_positions()
        for i in li_idx:
            pos[i] += rng.uniform(-args.perturb_A, args.perturb_A, 3)
        a.set_positions(pos)
        E = relax(a)
        dE_meV = (E - E_champion) * 1000
        flag = "✓ higher" if dE_meV > -1.0 else "❌ LOWER ← new basin"
        print(f"  trial {t:02d}: E={E:.4f}, dE={dE_meV:+.1f} meV  {flag}", flush=True)
        results.append({'trial': t, 'E_eV': E, 'dE_meV': dE_meV})

    deltas = [r['dE_meV'] for r in results]
    n_lower = sum(1 for d in deltas if d < -1.0)
    verdict = ("ROBUST: champion is local minimum within MLIP precision"
               if n_lower == 0 else
               f"NOT ROBUST: {n_lower}/{args.n_trials} trials found lower-E basin")

    summary = {
        'champion_xyz': args.champion,
        'E_champion_eV': E_champion,
        'n_trials': args.n_trials,
        'perturb_A': args.perturb_A,
        'seed': args.seed,
        'trials': results,
        'best_random_E_eV': min(r['E_eV'] for r in results),
        'best_random_dE_meV': min(deltas),
        'worst_random_dE_meV': max(deltas),
        'mean_dE_meV': float(np.mean(deltas)),
        'n_lower_than_champion': n_lower,
        'verdict': verdict,
    }
    with open(args.out_json, 'w') as f:
        json.dump(summary, f, indent=2)

    print("=" * 60)
    print(f"best dE  = {summary['best_random_dE_meV']:+.1f} meV")
    print(f"worst dE = {summary['worst_random_dE_meV']:+.1f} meV")
    print(f"mean dE  = {summary['mean_dE_meV']:+.1f} meV")
    print(f"n_lower  = {n_lower}/{args.n_trials}")
    print(f"VERDICT: {verdict}")
    print(f"→ {args.out_json}")

if __name__ == '__main__':
    main()
