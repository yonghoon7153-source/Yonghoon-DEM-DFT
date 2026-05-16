#!/usr/bin/env python
"""predict_new.py — given a NEW (compound, sites, concentration) combo,
score it instantly using the in-house ML predictors trained on the
cascade dataset.

Two modes:
  cold_start    — only label features (faster, less accurate). Use to
                  pre-filter "obviously bad" combos before launching UMA.
  with_structure — also feeds Tier-2 + BVSE metrics. Use AFTER a quick
                  UMA relax + BVSE pass on the candidate (~1 min) to get
                  a paper-tier prediction.

Usage:
  # Cold-start: just chemistry labels
  python3 tools/doping/predict_new.py \\
      --predictor_dir runs/.../predictor/ \\
      --dopant Nd2O3 --cation_site Li_24g --anion_site S_16e \\
      --concentration 0.05

  # With-structure: cheaper than full cascade, more accurate than cold
  python3 tools/doping/predict_new.py \\
      --predictor_dir runs/.../predictor/ \\
      --xyz path/to/candidate.xyz \\
      --dopant Nd2O3 --cation_site Li_24g --anion_site S_16e

Predictions are listed per target with a confidence band (CV R²).
"""
import argparse
import json
import pickle
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))


def compute_quick_features(xyz_path: Path) -> dict:
    """Tier-2 + BVSE features for a single xyz, no UMA call. Used by
    --with_structure mode."""
    from ase.io import read
    sys.path.insert(0, str(Path(__file__).parent))
    from run_uma_screening import compute_tier2_metrics
    from bvse_proxy import compute_bvs_per_li, compute_migration_volume
    a = read(str(xyz_path))
    tier2 = compute_tier2_metrics(a)
    bvs = compute_bvs_per_li(a)
    mig = compute_migration_volume(a, n_grid=20)
    return {
        'tier2_li_li_disorder_std': tier2['li_li_disorder_std'],
        'tier2_li_li_disorder_mean': tier2['li_li_disorder_mean'],
        'tier2_dopant_blocking_fraction': tier2['dopant_blocking_fraction'],
        'tier2_lattice_angle_dev_deg': tier2['lattice_angle_dev_deg'],
        'tier2_lattice_aspect_ratio': tier2['lattice_aspect_ratio'],
        'bvs_li_mean': bvs.get('bvs_li_mean'),
        'bvs_li_std': bvs.get('bvs_li_std'),
        'bvs_li_proxy_score': bvs.get('bvs_li_proxy_score'),
        'screen_dV_over_V0': 0.0,  # unknown for cold prediction
    }


def main():
    p = argparse.ArgumentParser(description=__doc__,
                               formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('--predictor_dir', required=True)
    p.add_argument('--dopant', required=True, help='e.g. Nd2O3')
    p.add_argument('--cation_site', default='Li_24g')
    p.add_argument('--anion_site', default='S_16e')
    p.add_argument('--concentration', type=float, default=0.05)
    p.add_argument('--charge_compensation', default='compound_set')
    p.add_argument('--n_fu_actual', type=int, default=4)
    p.add_argument('--xyz', help='Quick structure for with-structure mode')
    args = p.parse_args()

    pdir = Path(args.predictor_dir)
    models = {}
    for pkl_file in pdir.glob('predictor_*.pkl'):
        with pkl_file.open('rb') as f:
            models[pkl_file.stem.replace('predictor_', '')] = pickle.load(f)
    if not models:
        raise SystemExit(f"No predictor_*.pkl in {pdir}")
    summary = json.loads((pdir / 'training_summary.json').read_text())
    cv = summary.get('cv_metrics', {})

    # Build feature row
    row = {
        'dopant': args.dopant,
        'cation_site': args.cation_site,
        'anion_site': args.anion_site,
        'charge_compensation': args.charge_compensation,
        'concentration': args.concentration,
        'n_fu_actual': args.n_fu_actual,
    }
    if args.xyz:
        row.update(compute_quick_features(Path(args.xyz)))
        print(f"  (quick structural features added from {args.xyz})")

    df = pd.DataFrame([row])

    print(f"\n=== Prediction for {args.dopant} @ ({args.cation_site}, "
          f"{args.anion_site}), x={args.concentration} ===\n")
    print(f"{'Target':<35}{'Prediction':>14}{'CV R²':>10}{'CV MAE':>10}")
    print('-' * 70)
    for target, bundle in models.items():
        model = bundle['model']
        cat_feats = bundle['features_categorical']
        num_feats = bundle['features_numeric']
        # Build subset row with required features
        for f in cat_feats:
            if f not in df.columns:
                df[f] = 'unknown'
        for f in num_feats:
            if f not in df.columns:
                df[f] = 0.0
        X = df[cat_feats + num_feats]
        try:
            y_pred = model.predict(X)[0]
            tcv = cv.get(target, {})
            r2 = tcv.get('best_cv_r2_mean', tcv.get('cv_r2_mean', 0))
            mtype = bundle.get('model_type', 'gbr')
            print(f"{target:<35}{y_pred:>+13.4g} {r2:>+9.3f}  ({mtype})")
        except Exception as e:
            print(f"{target:<35}{'(predict err):':>14} {e}")
    print()


if __name__ == '__main__':
    main()
