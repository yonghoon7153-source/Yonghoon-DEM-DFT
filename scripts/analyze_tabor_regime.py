#!/usr/bin/env python3
"""Tabor regime analysis — compute μ_T = E*·a / (σ_y·R) per contact and
report the elastic / transitional / plastic distribution across the
80-case ensemble. Provides direct quantitative evidence for the Methods
section's elastic-plastic transition framing.

Tabor (1951) regime boundaries (per Brake 2012, Greenwood 1992):

  μ_T < 0.1       fully elastic         (Hertz applies)
  0.1 ≤ μ_T < 100 transitional          (mixed E-P, our solver picks min(A_H, A_T, A_vol))
  μ_T ≥ 100       fully plastic         (Hertz overestimates contact area)

Material constants — imported from scripts/plastic_coverage.py
(single source of truth for the entire DEM-postprocess pipeline):

  E_SE_real    = 24.0  GPa     (LPSCl lab value — Wang 2020, McGrogan 2017)
  ν_SE         = 0.30          (LIGGGHTS poissonsRatio for SE atom type)
  H_SE         = 0.85 GPa      (LPSCl Vickers, Sakuda 2013)
  σ_y_SE       = 0.30 GPa      (= H / 2.8, Tabor relation; not the textbook H/3)
  E*_SE-SE     = E / (2(1-ν²))  ≈ 13.2 GPa   (symmetric pair)

Note on E_SE: 24 GPa is the REAL lab value used for analytical Tabor /
volume / fracture post-corrections.  The DEM simulation itself uses a
softened E*_SE = 1.35 GPa to allow practical time steps; that softened
value is for the LIGGGHTS Hertzian contact during compaction only.
For per-contact μ_T evaluation we use the lab value (consistent with
plastic_coverage.py's `A_tabor = F_real / H_REAL_SE`).

Output
──────
  - Per-case median μ_T
  - Ensemble histogram (log scale) with regime bands
  - % of contacts in each regime
  - Optional matplotlib figure → docs/figures/tabor_regime_histogram.png
  - CSV summary → docs/db/tabor_regime_summary.csv

Usage
─────
  python3 scripts/analyze_tabor_regime.py
  python3 scripts/analyze_tabor_regime.py --pair SE-SE      # only SE-SE pairs
  python3 scripts/analyze_tabor_regime.py --plot            # save figure
  python3 scripts/analyze_tabor_regime.py CASE_ID …         # specific cases
"""
from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT     = Path(__file__).resolve().parent.parent
WEBAPP   = ROOT / 'webapp'
SCRIPTS  = ROOT / 'scripts'
DB_DIR   = ROOT / 'docs' / 'db'
FIG_DIR  = ROOT / 'docs' / 'figures'

# ── Material constants — single source of truth in plastic_coverage.py ──
sys.path.insert(0, str(SCRIPTS))
from plastic_coverage import (   # noqa: E402
    E_REAL_SE, E_REAL_AM, POISSON_SE, POISSON_AM,
    SIGMA_Y_SE, H_REAL_SE,
)

# Effective modulus for SE-SE symmetric pair  (1/E* = 2·(1-ν²)/E for symmetric)
E_STAR_SE_SE_PA = E_REAL_SE / (2.0 * (1.0 - POISSON_SE ** 2))

# Effective modulus for AM-AM symmetric pair (used if --pair AM-AM)
E_STAR_AM_AM_PA = E_REAL_AM / (2.0 * (1.0 - POISSON_AM ** 2))

# Effective modulus for AM-SE mixed pair  (1/E* = (1-ν₁²)/E₁ + (1-ν₂²)/E₂)
_inv_Estar = ((1 - POISSON_AM ** 2) / E_REAL_AM
              + (1 - POISSON_SE ** 2) / E_REAL_SE)
E_STAR_AM_SE_PA = 1.0 / _inv_Estar

# AM yield (from H_AM ≈ 6 GPa in fracture_model.py / H≈3σ_y for ceramics)
H_REAL_AM_PA = 6.0e9
SIGMA_Y_AM_PA = H_REAL_AM_PA / 3.0

# Regime boundaries (Brake 2012, Greenwood 1992 convention)
MU_T_ELASTIC_MAX = 0.1
MU_T_PLASTIC_MIN = 100.0


def discover_case_dirs() -> list[Path]:
    """Recursively find case dirs at any depth under results/ or archive/."""
    seen = set()
    out = []
    for base in ('results', 'archive'):
        root = WEBAPP / base
        if not root.exists():
            continue
        for atoms_p in root.rglob('atoms.csv'):
            case_dir = atoms_p.parent
            if ((case_dir / 'contacts.csv').exists()
                    and case_dir not in seen):
                seen.add(case_dir)
                out.append(case_dir)
    return sorted(out)


def _read_meta(case_dir: Path) -> dict:
    for path in (case_dir / 'meta.json',
                 WEBAPP / 'uploads' / case_dir.name / 'meta.json'):
        if path.exists():
            try:
                return json.load(open(path))
            except Exception:
                pass
    return {}


def _parse_type_map(s: str) -> dict:
    out = {}
    for tok in (s or '').split(','):
        if ':' in tok:
            k, v = tok.split(':', 1)
            try:
                out[int(k.strip())] = v.strip()
            except Exception:
                pass
    return out


def _e_star_sigma_y_for_pair(pair_label: str) -> tuple[float, float]:
    """Return (E*, σ_y) in Pa appropriate for a given pair type.

    For mixed AM-SE the soft side (SE) governs yield, mixed E* used.
    """
    if pair_label == 'SE-SE':
        return E_STAR_SE_SE_PA, SIGMA_Y_SE
    if pair_label == 'AM-AM':
        return E_STAR_AM_AM_PA, SIGMA_Y_AM_PA
    return E_STAR_AM_SE_PA, SIGMA_Y_SE   # AM-SE


def compute_mu_t_for_case(case_dir: Path, pair_filter: str | None = None
                           ) -> np.ndarray | None:
    """Return array of μ_T values for one case, optionally filtered by pair type.

    pair_filter ∈ {None, 'SE-SE', 'AM-AM', 'AM-SE'}.
    Uses simulation-unit contact_area and radius from contacts.csv + atoms.csv,
    converted to real m via meta.json scale.

    μ_T = E*·a / (σ_y·R) where E*, σ_y are pair-type-specific:
      SE-SE  : E*=13.2 GPa,  σ_y=0.30 GPa  (LPSCl)
      AM-AM  : E*=74.7 GPa,  σ_y=2.0 GPa   (NCM, H_AM ≈ 6 GPa)
      AM-SE  : E*=22.4 GPa,  σ_y=0.30 GPa  (mixed, soft side yields)
    """
    meta = _read_meta(case_dir)
    type_map = _parse_type_map(meta.get('type_map', '1:AM_P,2:AM_S,3:SE'))
    if not type_map:
        type_map = {1: 'AM_P', 2: 'AM_S', 3: 'SE'}
    scale = float(meta.get('scale', 1000))

    try:
        atoms = pd.read_csv(case_dir / 'atoms.csv',
                             usecols=['id', 'type', 'radius'])
        contacts = pd.read_csv(case_dir / 'contacts.csv', low_memory=False)
    except Exception:
        return None

    if 'contact_area' not in contacts.columns:
        return None

    # Build atom lookups
    id_to_type = dict(zip(atoms['id'].astype(int),
                            atoms['type'].astype(int)))
    id_to_radius_sim = dict(zip(atoms['id'].astype(int),
                                  atoms['radius'].astype(float)))

    # Pair filter (optional)
    am_types = {tid for tid, lbl in type_map.items() if 'AM' in str(lbl)}
    se_types = {tid for tid, lbl in type_map.items() if 'SE' in str(lbl)}

    mu_t_vals = []
    for _, c in contacts.iterrows():
        try:
            i1 = int(c['id1']); i2 = int(c['id2'])
        except Exception:
            continue
        t1 = id_to_type.get(i1); t2 = id_to_type.get(i2)
        if t1 is None or t2 is None:
            continue

        is_se_se = (t1 in se_types and t2 in se_types)
        is_am_am = (t1 in am_types and t2 in am_types)
        is_am_se = (t1 in am_types and t2 in se_types) or \
                   (t1 in se_types and t2 in am_types)

        if pair_filter == 'SE-SE' and not is_se_se:   continue
        if pair_filter == 'AM-AM' and not is_am_am:   continue
        if pair_filter == 'AM-SE' and not is_am_se:   continue

        ca_sim = float(c.get('contact_area') or 0.0)
        if ca_sim <= 0:
            continue

        # Convert sim → real meters
        # atoms.csv radius in sim units (m); real_m = sim_m / scale
        r1_real = id_to_radius_sim.get(i1, 0.0) / scale
        r2_real = id_to_radius_sim.get(i2, 0.0) / scale
        if r1_real <= 0 or r2_real <= 0:
            continue
        r_min = min(r1_real, r2_real)

        # contact_area in sim units (m²); real_m² = sim_m² / scale²
        ca_real_m2 = ca_sim / (scale ** 2)
        a_real = np.sqrt(ca_real_m2 / np.pi)
        if a_real <= 0:
            continue

        # μ_T = E*·a / (σ_y·R) — pair-type-specific E* and σ_y
        if is_se_se:    pair_str = 'SE-SE'
        elif is_am_am:  pair_str = 'AM-AM'
        else:           pair_str = 'AM-SE'
        E_star_pa, sigma_y_pa = _e_star_sigma_y_for_pair(pair_str)
        mu_t = (E_star_pa * a_real) / (sigma_y_pa * r_min)
        if np.isfinite(mu_t) and mu_t > 0:
            mu_t_vals.append(mu_t)

    return np.asarray(mu_t_vals) if mu_t_vals else None


def regime_breakdown(mu_t_arr: np.ndarray) -> dict:
    """Return % of contacts in elastic / transitional / plastic regimes."""
    n = len(mu_t_arr)
    if n == 0:
        return {'n': 0, 'pct_elastic': 0, 'pct_transit': 0, 'pct_plastic': 0,
                'median': float('nan'), 'mean': float('nan'),
                'q1': float('nan'), 'q3': float('nan')}
    pct_e = float(np.sum(mu_t_arr < MU_T_ELASTIC_MAX) / n * 100.0)
    pct_p = float(np.sum(mu_t_arr >= MU_T_PLASTIC_MIN) / n * 100.0)
    pct_t = 100.0 - pct_e - pct_p
    return {
        'n':            int(n),
        'pct_elastic':  round(pct_e, 2),
        'pct_transit':  round(pct_t, 2),
        'pct_plastic':  round(pct_p, 2),
        'median':       float(np.median(mu_t_arr)),
        'mean':         float(np.mean(mu_t_arr)),
        'q1':           float(np.percentile(mu_t_arr, 25)),
        'q3':           float(np.percentile(mu_t_arr, 75)),
    }


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('cases', nargs='*', help='Specific case_ids')
    ap.add_argument('--pair', choices=['SE-SE', 'AM-AM', 'AM-SE'],
                    default='SE-SE',
                    help='Restrict analysis to one pair type (default SE-SE)')
    ap.add_argument('--plot', action='store_true',
                    help='Save histogram figure to docs/figures/')
    ap.add_argument('--no-csv', action='store_true',
                    help='Skip per-case CSV output')
    args = ap.parse_args()

    # Pick E* and σ_y appropriate for the selected pair type
    if args.pair == 'SE-SE':
        E_star_pa = E_STAR_SE_SE_PA
        sigma_y_pa = SIGMA_Y_SE
        mat_label = 'SE'
        H_pa = H_REAL_SE
    elif args.pair == 'AM-AM':
        E_star_pa = E_STAR_AM_AM_PA
        sigma_y_pa = SIGMA_Y_AM_PA
        mat_label = 'AM'
        H_pa = H_REAL_AM_PA
    else:  # AM-SE — use mixed E*, soft side governs yield (= SE σ_y)
        E_star_pa = E_STAR_AM_SE_PA
        sigma_y_pa = SIGMA_Y_SE
        mat_label = 'AM-SE'
        H_pa = H_REAL_SE

    print(f'Tabor regime analysis  pair={args.pair}')
    print(f'  E*_{mat_label:<5s} = {E_star_pa/1e9:.2f} GPa')
    print(f'  σ_y_{mat_label:<5s} = {sigma_y_pa/1e9:.3f} GPa  '
          f'(H = {H_pa/1e9:.2f} GPa, H/σ_y = {H_pa/sigma_y_pa:.1f})')
    print(f'  Regimes:  elastic μ_T < {MU_T_ELASTIC_MAX}  | '
          f'transit  {MU_T_ELASTIC_MAX} ≤ μ_T < {MU_T_PLASTIC_MIN}  | '
          f'plastic μ_T ≥ {MU_T_PLASTIC_MIN}\n')

    all_cases = discover_case_dirs()
    if args.cases:
        wanted = set(args.cases)
        cases = [d for d in all_cases if d.name in wanted]
    else:
        cases = all_cases
    if not cases:
        ap.error('No cases found.')

    all_mu_t = []
    rows = []
    for d in cases:
        mu_t = compute_mu_t_for_case(d, pair_filter=args.pair)
        if mu_t is None or len(mu_t) == 0:
            print(f'  {d.name:35s}  [no {args.pair} contacts]')
            continue
        all_mu_t.append(mu_t)
        bd = regime_breakdown(mu_t)
        rows.append({'case_id': d.name, **bd})
        print(f'  {d.name:35s}  n={bd["n"]:6d}  '
              f'median μ_T={bd["median"]:7.3f}  '
              f'(E:{bd["pct_elastic"]:5.1f}% / '
              f'T:{bd["pct_transit"]:5.1f}% / '
              f'P:{bd["pct_plastic"]:5.1f}%)')

    if not all_mu_t:
        print('\nNo contacts found.')
        return

    pooled = np.concatenate(all_mu_t)
    bd = regime_breakdown(pooled)
    print(f'\n{"="*78}')
    print(f'Ensemble  ({args.pair}, n_cases={len(rows)})')
    print(f'{"="*78}')
    print(f'  Total contacts        : {bd["n"]}')
    print(f'  Median μ_T            : {bd["median"]:.3f}')
    print(f'  Mean μ_T              : {bd["mean"]:.3f}')
    print(f'  IQR (Q1–Q3)           : {bd["q1"]:.3f} – {bd["q3"]:.3f}')
    print(f'  % in fully elastic    : {bd["pct_elastic"]:.2f} % '
          f'(μ_T < {MU_T_ELASTIC_MAX})')
    print(f'  % in transitional     : {bd["pct_transit"]:.2f} % '
          f'({MU_T_ELASTIC_MAX} ≤ μ_T < {MU_T_PLASTIC_MIN})')
    print(f'  % in fully plastic    : {bd["pct_plastic"]:.2f} % '
          f'(μ_T ≥ {MU_T_PLASTIC_MIN})')

    interpretation = (
        'fully elastic'   if bd['pct_elastic'] > 80
        else 'fully plastic' if bd['pct_plastic'] > 80
        else 'TRANSITIONAL (Hertz vs Physics gap is meaningful)'
    )
    print(f'\n  Verdict: {args.pair} ensemble is in {interpretation} regime.')

    if not args.no_csv:
        DB_DIR.mkdir(parents=True, exist_ok=True)
        out_csv = DB_DIR / f'tabor_regime_{args.pair.replace("-", "")}.csv'
        pd.DataFrame(rows).to_csv(out_csv, index=False)
        print(f'\nWrote per-case summary  : {out_csv}')

    if args.plot:
        try:
            import matplotlib
            matplotlib.use('Agg')
            import matplotlib.pyplot as plt
        except ImportError:
            print('  (matplotlib not installed — skip --plot)')
            return
        FIG_DIR.mkdir(parents=True, exist_ok=True)
        bins = np.logspace(-3, 3, 60)
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.hist(pooled, bins=bins, color='gray', edgecolor='black',
                 linewidth=0.3)
        ax.axvspan(1e-3, MU_T_ELASTIC_MAX,  alpha=0.18, color='C0',
                    label=f'elastic (μ_T < {MU_T_ELASTIC_MAX})')
        ax.axvspan(MU_T_ELASTIC_MAX, MU_T_PLASTIC_MIN, alpha=0.18, color='C7',
                    label=f'transitional')
        ax.axvspan(MU_T_PLASTIC_MIN, 1e3, alpha=0.18, color='C3',
                    label=f'plastic (μ_T ≥ {MU_T_PLASTIC_MIN})')
        ax.axvline(bd['median'], color='black', linestyle='--', linewidth=1.2,
                    label=f'median = {bd["median"]:.2f}')
        ax.set_xscale('log')
        ax.set_xlabel('Tabor parameter  μ_T = E*·a / (σ_y·R)')
        ax.set_ylabel(f'# of {args.pair} contacts')
        ax.set_title(f'Tabor regime distribution — {args.pair} contacts, '
                       f'{len(rows)}-case ensemble')
        ax.legend(loc='upper right', fontsize=9)
        ax.grid(True, alpha=0.3, which='both')
        fig.tight_layout()
        out_png = FIG_DIR / f'tabor_regime_{args.pair.replace("-", "")}.png'
        fig.savefig(out_png, dpi=150)
        plt.close(fig)
        print(f'Wrote histogram         : {out_png}')


if __name__ == '__main__':
    main()
