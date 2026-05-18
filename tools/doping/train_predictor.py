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
    'sigma_300K_S_cm_NE',  # DT-5: Stage 10 σ_Li (paper-essential)
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
    p.add_argument('--models', nargs='+', default=['all'],
                  help="Which models to train. 'all' = every available "
                       "(gbr, rf, xgb if installed, lgbm if installed, "
                       "catboost if installed). For each target keep the "
                       "model with the highest CV R² as predictor_<target>.pkl.")
    args = p.parse_args()

    try:
        import pandas as pd
        from sklearn.ensemble import (GradientBoostingRegressor,
                                       RandomForestRegressor)
        from sklearn.dummy import DummyRegressor  # DT-6: baseline
        from sklearn.model_selection import (KFold, GroupKFold,
                                             LeaveOneGroupOut,
                                             cross_val_score)
        from sklearn.metrics import mean_absolute_error, r2_score
        from sklearn.preprocessing import OneHotEncoder
        from sklearn.compose import ColumnTransformer
        from sklearn.pipeline import Pipeline
        import pickle
    except ImportError as e:
        raise SystemExit(f"Need pandas + sklearn: {e}")

    # Optional fancier learners (auto-detect; skip silently if not installed)
    available_models = {
        'gbr': lambda: GradientBoostingRegressor(n_estimators=200,
                                                 max_depth=4, random_state=42),
        'rf':  lambda: RandomForestRegressor(n_estimators=300, max_depth=10,
                                             random_state=42, n_jobs=-1),
        # DT-6: dummy baseline — paper에 "GBR vs trivial baseline" 비교 가능
        'dummy': lambda: DummyRegressor(strategy='mean'),
    }
    try:
        from xgboost import XGBRegressor
        available_models['xgb'] = lambda: XGBRegressor(
            n_estimators=300, max_depth=5, learning_rate=0.05,
            random_state=42, n_jobs=-1, verbosity=0)
    except ImportError:
        pass
    try:
        from lightgbm import LGBMRegressor
        available_models['lgbm'] = lambda: LGBMRegressor(
            n_estimators=300, max_depth=-1, learning_rate=0.05,
            random_state=42, n_jobs=-1, verbose=-1)
    except ImportError:
        pass
    try:
        from catboost import CatBoostRegressor
        available_models['catboost'] = lambda: CatBoostRegressor(
            iterations=300, depth=5, learning_rate=0.05,
            random_state=42, verbose=False)
    except ImportError:
        pass
    print(f"Available models: {list(available_models.keys())}")

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
        # DT-4: groups for GroupKFold (dopant leakage prevention) + LOCO
        # (compound-level cold-start estimate).
        groups = d['dopant'].astype(str).values

        models_to_try = (list(available_models.keys())
                        if args.models == ['all']
                        else [m for m in args.models if m in available_models])
        if not models_to_try:
            print(f"  ✗ {tgt}: no available models")
            continue

        # DT-4: 3 CV schemes for paper-grade reporting.
        # 'random' KFold       — in-distribution (same dopant in train+test)
        #                        OPTIMISTIC, upper bound on production R².
        # 'group_dopant' GroupKFold — cold-start (dopant held out of fold).
        #                        REALISTIC for "new dopant" deployment.
        # 'loco' LeaveOneGroupOut — single dopant held out at a time.
        #                        PESSIMISTIC, true compound-level cold-start.
        cv_schemes = {
            'random': KFold(n_splits=5, shuffle=True, random_state=42),
        }
        n_groups = len(set(groups))
        if n_groups >= 3:
            cv_schemes['group_dopant'] = GroupKFold(
                n_splits=min(5, n_groups))
        if n_groups >= 2:
            cv_schemes['loco'] = LeaveOneGroupOut()

        target_results = {}
        best_model_name, best_r2, best_pipeline = None, -np.inf, None
        for mname in models_to_try:
            pre = ColumnTransformer([
                ('cat', OneHotEncoder(handle_unknown='ignore'),
                 feats_categorical),
            ], remainder='passthrough')
            pipeline = Pipeline([
                ('pre', pre),
                ('reg', available_models[mname]()),
            ])
            cv_per_scheme = {}
            for sname, sch in cv_schemes.items():
                try:
                    if sname == 'random':
                        r2 = cross_val_score(pipeline, X, y, cv=sch,
                                             scoring='r2')
                        mae = cross_val_score(pipeline, X, y, cv=sch,
                                              scoring='neg_mean_absolute_error')
                    else:
                        r2 = cross_val_score(pipeline, X, y, cv=sch,
                                             groups=groups, scoring='r2')
                        mae = cross_val_score(pipeline, X, y, cv=sch,
                                              groups=groups,
                                              scoring='neg_mean_absolute_error')
                    cv_per_scheme[sname] = {
                        'cv_r2_mean': float(r2.mean()),
                        'cv_r2_std': float(r2.std()),
                        'cv_mae_mean': float(-mae.mean()),
                        'n_folds': len(r2),
                    }
                except Exception as e:
                    cv_per_scheme[sname] = {'error': str(e)}

            # 'random' is the canonical CV for model selection (backward compat).
            random_r2 = cv_per_scheme.get('random', {}).get('cv_r2_mean')
            if random_r2 is None:
                print(f"    {mname}: random CV failed")
                continue
            target_results[mname] = {
                # Backward-compatible top-level (existing predict_new etc.
                # read 'cv_r2_mean'). Equals random KFold value.
                'cv_r2_mean': random_r2,
                'cv_r2_std': cv_per_scheme['random']['cv_r2_std'],
                'cv_mae_mean': cv_per_scheme['random']['cv_mae_mean'],
                # DT-4: 3 CV schemes for paper reporting
                'cv_by_scheme': cv_per_scheme,
            }
            if random_r2 > best_r2:
                best_r2 = random_r2
                best_model_name = mname
                best_pipeline = pipeline

        if best_pipeline is None:
            print(f"  ✗ {tgt}: all models failed")
            continue

        # Refit on full dataset and save the winning model
        best_pipeline.fit(X, y)
        with (out / f"predictor_{tgt}.pkl").open('wb') as f:
            pickle.dump({
                'model': best_pipeline,
                'model_type': best_model_name,
                'features_categorical': feats_categorical,
                'features_numeric': [f for f in feats_numeric if f in d.columns],
                'target': tgt,
            }, f)

        metrics[tgt] = {
            'n_rows': int(len(d)),
            'best_model': best_model_name,
            'best_cv_r2_mean': float(best_r2),
            'y_mean': float(y.mean()),
            'y_std': float(y.std()),
            'all_models': target_results,
        }
        mt = target_results[best_model_name]
        print(f"  ✓ {tgt}: best={best_model_name} "
              f"R²={mt['cv_r2_mean']:+.3f}±{mt['cv_r2_std']:.3f} "
              f"MAE={mt['cv_mae_mean']:.4g} "
              f"(tried {len(target_results)} models)")

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
