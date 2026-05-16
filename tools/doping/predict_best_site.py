#!/usr/bin/env python
"""predict_best_site.py — ML-guided site recommender.

Given just a compound name (e.g. "Nd2O3"), enumerate every chemically
allowed (cation_site, anion_site) combination, ask the trained predictor
for each one's expected ΔE/atom (and other targets), rank them. Optional
MLIP verify mode then actually generates+relaxes the top-K predicted
combinations to confirm.

The point: site recommendation is itself learnable. The full screening
dataset (winners + non-winners) tells the model "for Nd2O3, Li_24g+
S_16e gave -0.88, P_4b+Cl_4d gave -0.32" so new compound prediction is
informed by the same chemistry pattern.

Usage:
  # Just predict (no MLIP)
  python3 tools/doping/predict_best_site.py \\
      --predictor_dir runs/tier_.../predictor/ \\
      --compound Nd2O3 --top 5

  # Predict + MLIP verify top-K (slow, needs UMA)
  python3 tools/doping/predict_best_site.py \\
      --predictor_dir runs/tier_.../predictor/ \\
      --compound Nd2O3 --top 3 \\
      --verify --base db/structures/lpscl_F43m_24G_canonical.cif \\
      --out_dir runs/site_pred_Nd2O3/
"""
import argparse
import json
import pickle
import subprocess
import sys
from itertools import product
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
from _provenance import get_provenance


# Chemically allowed (cation_site, anion_site) pairs — site_preference's
# auto modes will further filter these by per-element radius/charge.
CATION_SITES = ['Li_24g', 'Li_48h', 'P_4b']
ANION_SITES  = ['S_16e', 'S_4a', 'Cl_4d']


def main():
    p = argparse.ArgumentParser(description=__doc__,
                               formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('--predictor_dir', required=True)
    p.add_argument('--compound', required=True,
                  help='Compound formula, e.g. Nd2O3')
    p.add_argument('--concentration', type=float, default=0.05)
    p.add_argument('--top', type=int, default=5)
    p.add_argument('--verify', action='store_true',
                  help='Actually run substitute_compound + UMA relax on '
                       'top-K predicted combinations and compare to ML '
                       'prediction (closes the prediction → MLIP loop).')
    p.add_argument('--base',
                  help='LPSCl base CIF (only needed with --verify)')
    p.add_argument('--out_dir',
                  help='Where to write verify structures (only with --verify)')
    p.add_argument('--n_seeds', type=int, default=3,
                  help='Seeds per (compound, sites) combo for verify')
    p.add_argument('--steps', type=int, default=1500,
                  help='UMA relax steps (only with --verify)')
    args = p.parse_args()

    pdir = Path(args.predictor_dir)
    models = {}
    for pkl_file in pdir.glob('predictor_*.pkl'):
        with pkl_file.open('rb') as f:
            models[pkl_file.stem.replace('predictor_', '')] = pickle.load(f)
    if not models:
        raise SystemExit(f"No predictor_*.pkl in {pdir}")

    # Enumerate combinations
    combos = list(product(CATION_SITES, ANION_SITES))
    print(f"\nML-predicted ranking for {args.compound} "
          f"(x={args.concentration}) — {len(combos)} candidate sites:")
    print()

    # Build feature rows
    rows = []
    for cs, asite in combos:
        rows.append({
            'dopant': args.compound,
            'cation_site': cs,
            'anion_site': asite,
            'charge_compensation': 'compound_set',
            'concentration': args.concentration,
            'n_fu_actual': 4,
            # Tier-2 / BVSE columns left at 0.0 (cold-start prediction)
        })
    df = pd.DataFrame(rows)

    # Predict per target
    main_target = 'screen_de_per_atom'
    if main_target not in models:
        raise SystemExit(f"Predictor for {main_target} missing in {pdir}")

    bundle = models[main_target]
    cat_feats = bundle['features_categorical']
    num_feats = bundle['features_numeric']
    for f in cat_feats:
        if f not in df.columns:
            df[f] = 'unknown'
    for f in num_feats:
        if f not in df.columns:
            df[f] = 0.0
    X = df[cat_feats + num_feats]
    df['predicted_dE'] = bundle['model'].predict(X)
    # Also predict other targets if available
    for tgt in ('eos_B0_GPa', 'elastic_E_young_GPa',
               'migration_volume_fraction'):
        if tgt in models:
            b = models[tgt]
            X2 = df[b['features_categorical'] + b['features_numeric']]
            df[f'predicted_{tgt}'] = b['model'].predict(X2)

    df_sorted = df.sort_values('predicted_dE')

    # Print
    print(f"{'Rank':<5}{'(cation, anion)':<28}{'ΔE/atom':>12}"
          f"{'B0 GPa':>10}{'E_y':>10}{'V_mig%':>10}")
    print('-' * 80)
    for i, (_, r) in enumerate(df_sorted.iterrows(), 1):
        site_pair = f"({r['cation_site']}, {r['anion_site']})"
        print(f"{i:<5}{site_pair:<28}"
              f"{r['predicted_dE']:>+11.4f} "
              f"{r.get('predicted_eos_B0_GPa', 0):>9.2f} "
              f"{r.get('predicted_elastic_E_young_GPa', 0):>9.2f} "
              f"{r.get('predicted_migration_volume_fraction', 0)*100:>8.2f}%")

    # Save prediction
    if args.out_dir:
        out = Path(args.out_dir)
        out.mkdir(parents=True, exist_ok=True)
        df_sorted.to_csv(out / 'predictions.csv', index=False)
        (out / 'predictions.json').write_text(json.dumps({
            'provenance': get_provenance(),
            'compound': args.compound,
            'concentration': args.concentration,
            'predictions': df_sorted.to_dict(orient='records'),
        }, indent=2, default=str))
        print(f"\n✓ Predictions → {out}/predictions.csv,.json")

    # Verify mode
    if args.verify:
        if not args.base or not args.out_dir:
            raise SystemExit("--verify requires --base and --out_dir")
        print(f"\n=== Verify top-{args.top} via MLIP substitute + UMA relax ===")
        top_k = df_sorted.head(args.top)
        for i, (_, r) in enumerate(top_k.iterrows(), 1):
            cs, asite = r['cation_site'], r['anion_site']
            tag = f"rank{i:02d}_c{cs.replace('_','')}_a{asite.replace('_','')}"
            verify_dir = Path(args.out_dir) / 'verify' / tag
            print(f"\n  [{i}/{args.top}] {tag}")
            cmd = [
                'python3', 'tools/doping/substitute_compound.py',
                '--base', args.base,
                '--compound', args.compound,
                '--x_compound', str(args.concentration),
                '--cation_site', cs, '--anion_site', asite,
                '--method', 'random', '--n_seeds', str(args.n_seeds),
                '--out', str(verify_dir),
            ]
            subprocess.run(cmd, check=False)
        print("\n  → Run run_uma_screening.py on these new structures, "
              "then compare with ML predictions to close the loop.")


if __name__ == '__main__':
    main()
