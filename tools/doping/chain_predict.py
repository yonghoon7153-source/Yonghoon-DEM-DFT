#!/usr/bin/env python
"""chain_predict.py — hierarchical (multi-tier) ML prediction with auto
go/no-go gating between tiers. The argyrodite digital-twin's prediction
side mirror of tier_cascade.sh's compute side.

Tier structure follows the natural dataset hierarchy:

  Tier 1  screen + anneal  ─  abundant data (every cascade structure)
                              targets: ΔE/atom (binding stability),
                              dV/V0, Tier-2 disorder metrics
  Tier 2  post-processing  ─  per-winner data (smaller subset)
                              targets: B0, V0, E_young, Pugh, ν,
                              migration_volume_fraction, BVSE proxy
  Tier 3  DFT (external)   ─  Top-K only; user runs on KISTI manually
                              (generate_dft_inputs.py prepares pw.in)

Predict workflow:
  1. Take a new (compound, cation_site, anion_site, conc) request
  2. Tier-1 predict ΔE/atom. If above --stability_threshold (i.e.
     unstable), STOP and report "rejected at Tier-1".
  3. Tier-2 predict B0, E_young, mobility. Report all values.
  4. If user passes --propose_dft, also report the composite score
     and a recommendation whether to spend DFT budget on this combo.

Usage:
  python3 tools/doping/chain_predict.py \\
      --predictor_dir runs/tier_.../predictor/ \\
      --compound Nd2O3 --cation_site Li_24g --anion_site S_16e \\
      --concentration 0.05
"""
import argparse
import json
import pickle
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
from _provenance import get_provenance


TIER_TARGETS = {
    1: ['screen_de_per_atom'],
    2: ['eos_B0_GPa', 'elastic_E_young_GPa', 'elastic_pugh_GoverB',
        'migration_volume_fraction'],
}


def predict_target(models, target, row):
    if target not in models:
        return None
    bundle = models[target]
    df = pd.DataFrame([row])
    for f in bundle['features_categorical']:
        if f not in df.columns:
            df[f] = 'unknown'
    for f in bundle['features_numeric']:
        if f not in df.columns:
            df[f] = 0.0
    X = df[bundle['features_categorical'] + bundle['features_numeric']]
    try:
        return float(bundle['model'].predict(X)[0])
    except Exception as e:
        return f"err: {e}"


def main():
    p = argparse.ArgumentParser(description=__doc__,
                               formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('--predictor_dir', required=True)
    p.add_argument('--compound', required=True)
    p.add_argument('--cation_site', default='Li_24g')
    p.add_argument('--anion_site', default='S_16e')
    p.add_argument('--concentration', type=float, default=0.05)
    p.add_argument('--n_fu_actual', type=int, default=4)
    p.add_argument('--charge_compensation', default='compound_set')
    # Tier gating thresholds
    p.add_argument('--stability_threshold', type=float, default=-0.01,
                  help='Tier-1 ΔE/atom must be ≤ this to proceed to Tier-2 '
                       '(default -0.01 eV/atom). v4.1 default of -0.05 was '
                       'too strict — empirical argyrodite doping ΔE/atom '
                       'falls in [-0.03, +0.02] (Mg/Al/Cl-rich literature), '
                       'so -0.05 rejected ~95%% of plausible candidates.')
    p.add_argument('--propose_dft', action='store_true',
                  help='Compute the composite score and recommend whether to '
                       'spend DFT budget (Tier-3) on this combination.')
    p.add_argument('--out', help='Save full prediction record to this JSON')
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

    # NEW-1 fix: cold-start WARN. If the requested compound is NOT in the
    # training set's dopant column, the OneHotEncoder maps it to a zero
    # vector (handle_unknown='ignore'); CV R² on in-distribution data
    # then no longer applies. We can't recover full reliability without
    # retraining, but at least we tell the user.
    training_dataset_csv = pdir.parent / 'dataset.csv'
    seen_dopants: set = set()
    if training_dataset_csv.exists():
        try:
            seen_dopants = set(pd.read_csv(training_dataset_csv,
                              usecols=['dopant'])['dopant'].dropna().unique())
        except Exception:
            pass
    is_ood = seen_dopants and args.compound not in seen_dopants
    if is_ood:
        print(f"\n⚠⚠⚠ COLD-START WARNING: '{args.compound}' is NOT in the "
              f"training set ({len(seen_dopants)} known dopants).")
        print(f"   The reported predictions are extrapolation; CV R² values "
              f"reflect in-distribution performance and DO NOT apply.")
        print(f"   Treat all numbers as ROUGH GUESSES and verify with a real "
              f"UMA cascade (e.g. predict_best_site --verify) before any "
              f"paper claim.")

    row = {
        'dopant': args.compound,
        'cation_site': args.cation_site,
        'anion_site': args.anion_site,
        'charge_compensation': args.charge_compensation,
        'concentration': args.concentration,
        'n_fu_actual': args.n_fu_actual,
    }

    result = {
        'provenance': get_provenance(),
        'input': row.copy(),
        'tiers': {},
    }

    print(f"\n=== Chain prediction for {args.compound} @ "
          f"({args.cation_site}, {args.anion_site}), x={args.concentration} ===")

    # Tier 1: screen-stage stability
    print(f"\n[Tier 1] screen-stage stability check "
          f"(reject if ΔE/atom > {args.stability_threshold:+.4f} eV)")
    tier1_results = {}
    for tgt in TIER_TARGETS[1]:
        v = predict_target(models, tgt, row)
        r2 = cv.get(tgt, {}).get('best_cv_r2_mean', 0)
        tier1_results[tgt] = {'value': v, 'cv_r2': r2}
        if isinstance(v, (int, float)):
            print(f"  {tgt:<35}{v:>+13.4g}  (CV R²={r2:+.3f})")
        else:
            print(f"  {tgt:<35}{str(v):<25}")
    result['tiers']['tier_1'] = tier1_results

    de = tier1_results.get('screen_de_per_atom', {}).get('value')
    if not isinstance(de, (int, float)) or de > args.stability_threshold:
        verdict = 'REJECTED at Tier-1 (insufficient stability)'
        result['final_verdict'] = verdict
        print(f"\n→ {verdict}\n   Not advancing to Tier-2.")
        if args.out:
            Path(args.out).write_text(json.dumps(result, indent=2, default=str))
        return

    print(f"\n  ✓ Passed Tier-1 (ΔE/atom = {de:+.4f} ≤ {args.stability_threshold:+.4f})")

    # Tier 2: post-processing properties
    print(f"\n[Tier 2] post-processing property prediction")
    tier2_results = {}
    for tgt in TIER_TARGETS[2]:
        v = predict_target(models, tgt, row)
        r2 = cv.get(tgt, {}).get('best_cv_r2_mean', 0)
        tier2_results[tgt] = {'value': v, 'cv_r2': r2}
        if isinstance(v, (int, float)):
            print(f"  {tgt:<35}{v:>+13.4g}  (CV R²={r2:+.3f})")
    result['tiers']['tier_2'] = tier2_results

    # Composite score for paper objective (stability 0.4 + modulus 0.3 + mobility 0.3)
    if args.propose_dft:
        ey = tier2_results.get('elastic_E_young_GPa', {}).get('value', 0) or 0
        mob = (tier2_results.get('migration_volume_fraction', {}).get('value', 0)
               or 0)
        # NEW-3 fix: derive normalization from the ACTUAL training
        # dataset min/max instead of hard-coded ranges. Falls back to
        # narrow empirical ranges only if dataset.csv is missing.
        # M-3 fix (2026-05-16): fallback ranges narrowed to argyrodite-
        # doping literature values (Mg/Al/Cl-rich/Nd2O3 typical):
        #   ΔE/atom ∈ [-0.05, +0.02]  (was [-1.5, +0.5] which over-spread)
        #   E_young  ∈ [15, 40] GPa   (LPSCl D'Amore 2022, Pustorino 2025)
        #   mob frac ∈ [0, 0.15]      (BVSE on canonical structures)
        # Cascade always produces dataset.csv at stage 09b so this path
        # is only used in unusual circumstances (predictor copied alone).
        norm_ranges = {
            'screen_de_per_atom':           (-0.05, 0.02),
            'elastic_E_young_GPa':          (15, 40),
            'migration_volume_fraction':    (0, 0.15),
        }
        if training_dataset_csv.exists():
            try:
                df_train = pd.read_csv(training_dataset_csv)
                for col in norm_ranges:
                    if col in df_train.columns:
                        vals = df_train[col].dropna()
                        if len(vals) > 5:
                            norm_ranges[col] = (float(vals.min()),
                                               float(vals.max()))
            except Exception:
                pass
        de_lo, de_hi = norm_ranges['screen_de_per_atom']
        ey_lo, ey_hi = norm_ranges['elastic_E_young_GPa']
        mb_lo, mb_hi = norm_ranges['migration_volume_fraction']
        stab_score = (max(0, min((de_hi - de) / max(de_hi - de_lo, 1e-6), 1))
                     if isinstance(de, (int, float)) else 0)
        mod_score = max(0, min((ey - ey_lo) / max(ey_hi - ey_lo, 1e-6), 1))
        mob_score = max(0, min((mob - mb_lo) / max(mb_hi - mb_lo, 1e-6), 1))
        composite = 0.4 * stab_score + 0.3 * mod_score + 0.3 * mob_score
        result['composite_score'] = composite
        result['composite_norm_ranges'] = norm_ranges
        result['dft_recommended'] = composite > 0.5
        result['cold_start_warning'] = is_ood
        print(f"\n[Tier 3 gating]")
        print(f"  composite paper score: {composite:.3f}")
        print(f"  norm ranges (from dataset if available):")
        for k, v in norm_ranges.items():
            print(f"    {k:<35} {v}")
        if is_ood:
            print(f"  DFT recommended: NO (cold-start, do not waste DFT budget)")
        else:
            print(f"  DFT recommended: {'YES' if composite > 0.5 else 'no'} "
                  f"(threshold 0.50)")

    result['final_verdict'] = 'passed Tier-1+2'
    if args.out:
        Path(args.out).write_text(json.dumps(result, indent=2, default=str))
        print(f"\nFull record → {args.out}")


if __name__ == '__main__':
    main()
