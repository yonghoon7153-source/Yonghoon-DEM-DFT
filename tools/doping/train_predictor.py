#!/usr/bin/env python
"""train_predictor.py — train an in-house ML predictor on the cascade
dataset so that NEW (compound, sites, concentration) combinations can be
scored in seconds without running the full UMA + anneal + EOS chain.

Approach:
  - Features: dopant + site labels (one-hot), composition counts,
              Tier-2 metrics + BVSE proxy (cheap, available before
              heavy stages)
  - Targets: ΔE/atom (binding), B0 (modulus), E_young, Pugh,
              migration_volume_fraction (Li mobility)
  - Model: scikit-learn GradientBoostingRegressor per target (deterministic,
              no GPU, fast to retrain when dataset grows)
  - Outputs:
      predictor_<target>.pkl — trained model
      feature_columns.json — column order used by predict_new.py
      cv_metrics.json — 5-fold CV R²/MAE/RMSE per target

Long-term: when dataset grows to >10k structures, swap GBR for ALIGNN
or M3GNet GNN model (graph-based, sees crystal structure directly).

Usage:
  python3 tools/doping/train_predictor.py \\
      --csv runs/tier_.../dataset.csv \\
      --out_dir runs/tier_.../predictor/
"""
import argparse
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
from _provenance import get_provenance


TARGETS = [
    'screen_de_per_atom',
    'eos_B0_GPa',
    'elastic_E_young_GPa',
    'elastic_pugh_GoverB',
    'migration_volume_fraction',
]

# Features computable from a NEW (compound, sites, conc) request without UMA
CHEAP_FEATURES = [
    # Categorical (one-hot encoded downstream)
    'dopant', 'cation_site', 'anion_site', 'charge_compensation',
    # Numeric
    'concentration', 'n_fu_actual',
]

# Features that need UMA (used only as additional inputs for "predict
# given screening already done"; not for cold-start prediction)
STRUCTURAL_FEATURES = [
    'screen_dV_over_V0',
    'tier2_li_li_disorder_std', 'tier2_li_li_disorder_mean',
    'tier2_dopant_blocking_fraction', 'tier2_lattice_angle_dev_deg',
    'tier2_lattice_aspect_ratio',
    'bvs_li_mean', 'bvs_li_std', 'bvs_li_proxy_score',
]


def main():
    p = argparse.ArgumentParser(description=__doc__,
                               formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('--csv', required=True)
    p.add_argument('--out_dir', required=True)
    p.add_argument('--mode', choices=['cold_start', 'with_structure'],
                  default='with_structure',
                  help="'cold_start': only label features (predict before UMA), "
                       "'with_structure': also use Tier-2 + BVSE (predict after "
                       "a quick UMA + BVSE pass).")
    args = p.parse_args()

    try:
        import pandas as pd
        from sklearn.ensemble import GradientBoostingRegressor
        from sklearn.model_selection import KFold, cross_val_score
        from sklearn.metrics import mean_absolute_error, r2_score
        from sklearn.preprocessing import OneHotEncoder
        from sklearn.compose import ColumnTransformer
        from sklearn.pipeline import Pipeline
        import pickle
    except ImportError as e:
        raise SystemExit(f"Need pandas + sklearn: {e}")

    out = Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(args.csv)
    print(f"Loaded {len(df)} rows × {len(df.columns)} columns")

    feats_categorical = ['dopant', 'cation_site', 'anion_site',
                        'charge_compensation']
    feats_numeric = ['concentration', 'n_fu_actual']
    if args.mode == 'with_structure':
        feats_numeric += STRUCTURAL_FEATURES

    metrics = {}
    for tgt in TARGETS:
        if tgt not in df.columns:
            print(f"  ✗ skip {tgt} (column missing)")
            continue
        mask = df[tgt].notna()
        for f in feats_categorical:
            mask &= df[f].notna()
        for f in feats_numeric:
            if f in df.columns:
                mask &= df[f].notna()
        d = df[mask]
        if len(d) < 20:
            print(f"  ✗ skip {tgt} (only {len(d)} usable rows)")
            continue

        X = d[feats_categorical + [f for f in feats_numeric if f in d.columns]]
        y = d[tgt].values

        pre = ColumnTransformer([
            ('cat', OneHotEncoder(handle_unknown='ignore'), feats_categorical),
        ], remainder='passthrough')
        model = Pipeline([
            ('pre', pre),
            ('reg', GradientBoostingRegressor(n_estimators=200,
                                              max_depth=4, random_state=42))
        ])

        # 5-fold CV
        kf = KFold(n_splits=5, shuffle=True, random_state=42)
        cv_r2 = cross_val_score(model, X, y, cv=kf, scoring='r2')
        cv_mae = cross_val_score(model, X, y, cv=kf, scoring='neg_mean_absolute_error')

        # Train final model on all data
        model.fit(X, y)
        with (out / f"predictor_{tgt}.pkl").open('wb') as f:
            pickle.dump({'model': model, 'features_categorical': feats_categorical,
                        'features_numeric': [f for f in feats_numeric if f in d.columns],
                        'target': tgt}, f)

        metrics[tgt] = {
            'n_rows': int(len(d)),
            'cv_r2_mean': float(cv_r2.mean()),
            'cv_r2_std': float(cv_r2.std()),
            'cv_mae_mean': float(-cv_mae.mean()),
            'y_mean': float(y.mean()),
            'y_std': float(y.std()),
        }
        print(f"  ✓ {tgt}: n={len(d)} R²={cv_r2.mean():+.3f}±{cv_r2.std():.3f} "
              f"MAE={-cv_mae.mean():.4g} (y_mean={y.mean():+.3g}, σ={y.std():.3g})")

    summary = {
        'provenance': get_provenance(),
        'mode': args.mode,
        'features_categorical': feats_categorical,
        'features_numeric': feats_numeric,
        'targets_trained': list(metrics.keys()),
        'cv_metrics': metrics,
    }
    (out / 'training_summary.json').write_text(
        json.dumps(summary, indent=2, default=str))
    print(f"\n✓ {len(metrics)} models → {out}/predictor_*.pkl")
    print(f"  Summary → {out}/training_summary.json")


if __name__ == '__main__':
    main()
