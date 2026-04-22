#!/usr/bin/env python3
"""
PLASTIC_IMPACT_ON_PARAMETERS study.

Compares Hertzian vs Physics-mode values for every structural and
transport parameter we have dual-mode data on, across the 60-case
dataset. Purpose: decide whether plastic-deformation treatment (E_eff
calibration + Tabor caps) shifts STRUCTURAL descriptors (coverage, CN,
φ_SE, τ_Dij) or only σ-level transport properties.

Three hypotheses from packing_regime_db.json:
  H1  coverage increases in plastic (A_plastic > A_hertzian)  → shifts
      scaling-law cov^(2/5) term
  H2  CN unchanged (topology-defined, mode-agnostic)
  H3  τ_Dij unchanged (geodesic, mode-agnostic)

Outputs:
  docs/figures/physics_regime/plastic_impact_delta.csv    per-case Δ%
  docs/figures/physics_regime/plastic_impact_summary.csv  per-param stats
  docs/figures/physics_regime/plastic_impact_histograms.png
  stdout summary table

Usage:
  python3 scripts/plastic_impact_on_params.py
  python3 scripts/plastic_impact_on_params.py --regime-stratify  # split by geometric/transition/plastic
"""
from __future__ import annotations
import os, json, sys, argparse
from pathlib import Path
import numpy as np
import pandas as pd

WEBAPP = Path(__file__).parent.parent / 'webapp'
OUT = Path('docs/figures/physics_regime')
OUT.mkdir(parents=True, exist_ok=True)


# σ-related parameters that have dual-mode (_physics suffix) entries.
DUAL_SIGMA_KEYS = [
    ('sigma_full_mScm',             'σ_ionic (mS/cm)'),
    ('sigma_bulk_net_mScm',         'σ_bulk_net (mS/cm)'),
    ('electronic_sigma_full_mScm',  'σ_electronic (mS/cm)'),
    ('thermal_sigma_full_mScm',     'σ_thermal (mS/cm)'),
    ('R_brug_over_full',            'R_Brug / R_full ratio'),
    ('bulk_resistance_fraction',    'R_bulk fraction'),
]

# Structural parameters that SHOULD be mode-agnostic (H2/H3 test).
STRUCTURAL_KEYS = [
    ('phi_se',           'φ_SE'),
    ('porosity',         'porosity (%)'),
    ('thickness_um',     'thickness (μm)'),
    ('se_se_cn',         'SE-SE CN mean'),
    ('tortuosity_mean',  'τ_Dij (geodesic)'),
    ('percolation_pct',  'percolation (%)'),
]

# Coverage parameters (H1 test): if Physics mode A > Hertzian mode A, does
# coverage computed from these A's also differ? Requires plastic_coverage
# to have been run in both modes (may not be available for all cases).
COVERAGE_KEYS = [
    ('coverage_AM_P_mean',  'coverage AM_P (%)'),
    ('coverage_AM_S_mean',  'coverage AM_S (%)'),
    ('coverage_AM_mean',    'coverage AM total (%)'),
]


def load_metrics(case_dir: Path) -> dict | None:
    p = case_dir / 'full_metrics.json'
    if not p.exists():
        return None
    try:
        return json.load(open(p))
    except Exception:
        return None


def case_name(case_id: str) -> str:
    for base in (WEBAPP / 'uploads', WEBAPP / 'results'):
        m = base / case_id / 'meta.json'
        if m.exists():
            try:
                return json.load(open(m)).get('name', case_id)
            except Exception:
                pass
    return case_id


def regime_label(p50_dr: float, geom_pct: float) -> str:
    """3-regime classification from packing_regime_empirical_map."""
    if geom_pct >= 10 and p50_dr >= 0.25:
        return 'plastic-dominated'
    if p50_dr <= 0.20 and geom_pct < 2:
        return 'geometric'
    return 'transition'


def pct_delta(h, p):
    if h is None or p is None:
        return None
    try:
        h = float(h); p = float(p)
        if abs(h) < 1e-12:
            return None
        return (p - h) / abs(h) * 100.0
    except Exception:
        return None


def build_rows():
    """Iterate every case with dual-mode (_physics) data."""
    # Regime table for stratification
    reg_csv = OUT / 'dataset_summary.csv'
    reg_map = {}
    if reg_csv.exists():
        for _, r in pd.read_csv(reg_csv).iterrows():
            reg_map[r['case_id']] = {
                'p50_dr':   r.get('p50_dr', 0),
                'geom_pct': r.get('geom', 0),
                'tabor_pct': r.get('tabor', 0),
                'liggghts_lb_pct': r.get('liggghts_lb', 0),
            }

    rows = []
    for base in (WEBAPP / 'results', WEBAPP / 'archive'):
        if not base.is_dir():
            continue
        for d in sorted(base.iterdir()):
            if not d.is_dir():
                continue
            m = load_metrics(d)
            if not m:
                continue
            # Require at least one dual-mode key populated
            has_dual = any((k + '_physics') in m and m[k + '_physics'] is not None
                            for k, _ in DUAL_SIGMA_KEYS)
            if not has_dual:
                continue

            cid = d.name
            reg = reg_map.get(cid, {})
            row = {
                'case_id': cid,
                'name':    case_name(cid),
                'p50_dr':  reg.get('p50_dr', 0),
                'geom_pct': reg.get('geom_pct', 0),
                'regime':  regime_label(reg.get('p50_dr', 0), reg.get('geom_pct', 0)),
            }
            # σ-family Δ
            for key, _ in DUAL_SIGMA_KEYS:
                h = m.get(key)
                p = m.get(key + '_physics')
                row[f'{key}_H']     = h
                row[f'{key}_P']     = p
                row[f'{key}_dpct']  = pct_delta(h, p)
            # Structural (single value — must be identical in both modes)
            for key, _ in STRUCTURAL_KEYS:
                row[f'{key}'] = m.get(key)
            # Coverage (single value — but if we later re-run plastic_coverage
            # in physics mode we can add _physics version)
            for key, _ in COVERAGE_KEYS:
                row[key] = m.get(key)
            rows.append(row)
    return rows


def print_stdout_summary(df: pd.DataFrame, args):
    print(f"\n=== PLASTIC_IMPACT_ON_PARAMETERS  —  {len(df)} cases with dual-mode data ===\n")

    print("── σ-family Δ% (physics − hertzian)/hertzian ──")
    print(f"  {'parameter':28s} {'median':>8s} {'mean':>8s} {'p90':>8s} {'max':>8s}  n_nonzero")
    for key, label in DUAL_SIGMA_KEYS:
        col = f'{key}_dpct'
        vals = df[col].dropna().values
        if len(vals) == 0:
            continue
        nz = int(np.sum(np.abs(vals) > 0.05))  # |Δ| > 0.05%
        print(f"  {label:28s} {np.median(vals):+7.2f}% {np.mean(vals):+7.2f}% "
              f"{np.percentile(np.abs(vals), 90):7.2f}% {np.max(np.abs(vals)):7.2f}%   "
              f"{nz}/{len(vals)}")

    print("\n── Structural (H2/H3 test: should all be mode-agnostic) ──")
    print("  (These values are identical across modes by construction — listed here for reference)")
    for key, label in STRUCTURAL_KEYS:
        vals = df[key].dropna().values
        if len(vals) == 0:
            continue
        print(f"  {label:28s}  range [{np.min(vals):7.3f} , {np.max(vals):7.3f}]   mean={np.mean(vals):.3f}")

    print("\n── Regime-stratified σ_ionic Δ% ──")
    for reg in ['geometric', 'transition', 'plastic-dominated']:
        sub = df[df['regime'] == reg]
        if len(sub) == 0:
            continue
        col = 'sigma_full_mScm_dpct'
        vals = sub[col].dropna().values
        if len(vals) == 0:
            continue
        print(f"  {reg:22s}  n={len(sub):2d}  "
              f"Δσ_ionic median={np.median(vals):+6.2f}%  "
              f"mean={np.mean(vals):+6.2f}%  "
              f"max={np.max(np.abs(vals)):6.2f}%")

    if args.regime_stratify:
        print("\n── Full by-regime breakdown ──")
        for reg in ['geometric', 'transition', 'plastic-dominated']:
            sub = df[df['regime'] == reg]
            if len(sub) == 0:
                continue
            print(f"\n  [{reg}]  n={len(sub)}")
            for key, label in DUAL_SIGMA_KEYS:
                vals = sub[f'{key}_dpct'].dropna().values
                if len(vals):
                    print(f"    {label:28s} median Δ = {np.median(vals):+7.2f}%  "
                          f"max |Δ| = {np.max(np.abs(vals)):6.2f}%")


def plot_histograms(df: pd.DataFrame):
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
    except Exception:
        return

    fig, axes = plt.subplots(2, 3, figsize=(14, 8))
    for ax, (key, label) in zip(axes.flat, DUAL_SIGMA_KEYS):
        col = f'{key}_dpct'
        vals = df[col].dropna().values
        if len(vals) == 0:
            ax.axis('off'); continue
        regimes = df.loc[df[col].notna(), 'regime'].values
        colors = {'geometric': '#60a5fa', 'transition': '#fbbf24',
                   'plastic-dominated': '#ef4444'}
        for reg in ('geometric', 'transition', 'plastic-dominated'):
            mask = regimes == reg
            if np.any(mask):
                ax.hist(vals[mask], bins=20, color=colors[reg], alpha=0.6,
                        label=f'{reg} (n={int(mask.sum())})', edgecolor='white')
        ax.axvline(0, color='k', lw=0.7, ls='--')
        ax.set_xlabel(f'Δ% (physics − hertzian)/hertzian')
        ax.set_title(label, fontsize=9)
        ax.legend(fontsize=7, framealpha=0.9)
        ax.grid(alpha=0.2)
    plt.suptitle(f'Plastic-deformation impact on parameters  (n={len(df)} cases)',
                  fontsize=11, fontweight='bold')
    plt.tight_layout()
    p = OUT / 'plastic_impact_histograms.png'
    fig.savefig(p, dpi=150)
    plt.close()
    print(f"\n→ {p}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--regime-stratify', action='store_true',
                    help='Print full by-regime breakdown of every parameter')
    args = ap.parse_args()

    rows = build_rows()
    if not rows:
        print("ERROR: no cases found with dual-mode data. "
              "Run contact-mode=both analysis first "
              "(scripts/run_all_network.py --contact-mode both).")
        sys.exit(1)

    df = pd.DataFrame(rows)
    # Save full per-case Δ table
    p_csv = OUT / 'plastic_impact_delta.csv'
    df.to_csv(p_csv, index=False)
    print(f"→ {p_csv}")

    # Summary per-parameter
    summary_rows = []
    for key, label in DUAL_SIGMA_KEYS:
        vals = df[f'{key}_dpct'].dropna().values
        if len(vals) == 0:
            continue
        summary_rows.append({
            'parameter': label,
            'key': key,
            'n': int(len(vals)),
            'median_dpct': float(np.median(vals)),
            'mean_dpct':   float(np.mean(vals)),
            'p90_abs_dpct': float(np.percentile(np.abs(vals), 90)),
            'max_abs_dpct': float(np.max(np.abs(vals))),
            'n_significant': int(np.sum(np.abs(vals) > 5)),  # |Δ|>5% threshold
        })
    s_csv = OUT / 'plastic_impact_summary.csv'
    pd.DataFrame(summary_rows).to_csv(s_csv, index=False)
    print(f"→ {s_csv}")

    print_stdout_summary(df, args)
    plot_histograms(df)

    # Verdict
    print("\n" + "=" * 70)
    print("VERDICT")
    print("=" * 70)
    sig_med = df['sigma_full_mScm_dpct'].dropna().median()
    sig_max = df['sigma_full_mScm_dpct'].dropna().abs().max() if df['sigma_full_mScm_dpct'].notna().any() else 0
    print(f"σ_ionic: median Δ = {sig_med:+.2f}%,  max |Δ| = {sig_max:.2f}%")
    if abs(sig_med) < 1 and sig_max < 10:
        print("  → Plastic correction is small for most cases. Hertzian primary is SAFE.")
    elif sig_max > 20:
        print("  → Plastic correction is substantial in some regimes. Physics sensitivity band recommended in SI.")
    else:
        print("  → Moderate correction. Report both as main-text primary + SI sensitivity.")


if __name__ == '__main__':
    main()
