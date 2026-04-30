#!/usr/bin/env python3
"""Section 7 — Fracture-aware σ_e regression and Pareto-frontier analysis.

Aggregates Stage C (run_network_fracture_aware.py) outputs across the
78-case ensemble and quantifies:

  1. σ_e_loss_pct distribution (overall + per r_SE band)
  2. r_SE → σ_e_loss_pct regression
  3. P:S ratio → σ_e_loss_pct regression
  4. AM_P severe% → σ_e_loss_pct regression
  5. 3-objective Pareto frontier (σ_ionic, σ_e_fracture_aware, severe%)

Output:
  docs/db/section7_fracture_aware_summary.csv
  console summary tables (paper-grade prose anchors)
"""
from __future__ import annotations
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
WEBAPP = ROOT / 'webapp'
DB_DIR = ROOT / 'docs' / 'db'


def discover_case_dirs() -> list[Path]:
    out = []
    for base in ('results', 'archive'):
        root = WEBAPP / base
        if not root.exists():
            continue
        for d in sorted(root.iterdir()):
            if d.is_dir() and (d / 'full_metrics.json').exists():
                out.append(d)
    return out


def _read_meta(case_dir: Path) -> dict:
    for path in (case_dir / 'meta.json',
                 WEBAPP / 'uploads' / case_dir.name / 'meta.json'):
        if path.exists():
            try:
                return json.load(open(path))
            except Exception:
                pass
    return {}


def _parse_ps_ratio(meta: dict) -> tuple[float, str]:
    """Return (am_p_volume_fraction_within_AM, label) — e.g. (0.7, '7:3')."""
    ps = meta.get('ps_ratio') or meta.get('p_s_ratio') or meta.get('mass_ratio')
    if ps is None:
        return float('nan'), ''
    if isinstance(ps, (int, float)):
        return float(ps), str(ps)
    s = str(ps).strip()
    if ':' in s:
        try:
            p, q = s.split(':', 1)
            p, q = float(p), float(q)
            return p / (p + q), s
        except Exception:
            pass
    try:
        return float(s), s
    except Exception:
        return float('nan'), s


def _parse_se_radius(meta: dict, atoms_radii: dict) -> float:
    r = meta.get('r_SE') or meta.get('se_radius') or meta.get('SE_radius')
    if r is not None:
        try:
            return float(r)
        except Exception:
            pass
    for k, v in atoms_radii.items():
        if 'SE' in str(k):
            return float(v)
    return float('nan')


def _se_radius_from_atoms(case_dir: Path, type_map: dict) -> float:
    p = case_dir / 'atoms.csv'
    if not p.exists():
        return float('nan')
    try:
        df = pd.read_csv(p, usecols=['type', 'radius'])
    except Exception:
        return float('nan')
    se_types = [int(tid) for tid, lbl in type_map.items() if 'SE' in str(lbl)]
    if not se_types:
        return float('nan')
    sub = df[df['type'].isin(se_types)]
    if sub.empty:
        return float('nan')
    return float(sub['radius'].median())


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


def aggregate() -> pd.DataFrame:
    cases = discover_case_dirs()
    rows = []
    for d in cases:
        try:
            with open(d / 'full_metrics.json') as f:
                fm = json.load(f)
        except Exception as e:
            print(f'  skip {d.name}: fm read failed: {e}', file=sys.stderr)
            continue
        meta = _read_meta(d)
        ps_frac, ps_label = _parse_ps_ratio(meta)
        type_map = _parse_type_map(meta.get('type_map', '1:AM_P,2:AM_S,3:SE'))
        r_SE = _se_radius_from_atoms(d, type_map)
        rows.append({
            'case_id': d.name,
            'ps_label': ps_label,
            'ps_frac_AM_P': ps_frac,
            'r_SE_um': r_SE,
            'porosity': fm.get('porosity'),
            'percolation_pct': fm.get('percolation_pct') or fm.get('top_reachable_pct'),
            'sigma_ionic_full': fm.get('sigma_full_mScm'),
            'sigma_ionic_physics': fm.get('sigma_full_mScm_physics'),
            'sigma_e_full': fm.get('electronic_sigma_full_mScm'),
            'sigma_e_fracture_aware': fm.get('electronic_sigma_full_mScm_fracture_aware'),
            'sigma_e_loss_pct': fm.get('electronic_sigma_loss_pct'),
            'sigma_th_full': fm.get('thermal_sigma_full_mScm'),
            'sigma_th_fracture_aware': fm.get('thermal_sigma_full_mScm_fracture_aware'),
            'sigma_th_loss_pct': fm.get('thermal_sigma_loss_pct'),
            'frac_severe_pct': fm.get('frac_severe_pct'),
            'frac_severe_force_pct': fm.get('frac_severe_force_pct'),
            'frac_AM_P_AM_P_severe_pct': fm.get('frac_AM_P_AM_P_severe_pct'),
            'frac_AM_P_AM_P_severe_force_pct': fm.get('frac_AM_P_AM_P_severe_force_pct'),
            'fracture_index': fm.get('fracture_index'),
            'fracture_index_force': fm.get('fracture_index_force'),
            'n_am_am_contacts_total': fm.get('n_am_am_contacts_total'),
            'n_am_am_contacts_excluded': fm.get('n_am_am_contacts_excluded'),
            'fracture_aware_excluded_pct': fm.get('fracture_aware_excluded_pct'),
        })
    return pd.DataFrame(rows)


def _pearson(x, y):
    x = np.asarray(x, float); y = np.asarray(y, float)
    m = ~(np.isnan(x) | np.isnan(y))
    if m.sum() < 5: return float('nan'), int(m.sum())
    x, y = x[m], y[m]
    if x.std() == 0 or y.std() == 0: return float('nan'), len(x)
    return float(np.corrcoef(x, y)[0, 1]), len(x)


def _spearman(x, y):
    x = np.asarray(x, float); y = np.asarray(y, float)
    m = ~(np.isnan(x) | np.isnan(y))
    if m.sum() < 5: return float('nan'), int(m.sum())
    x, y = x[m], y[m]
    rx = pd.Series(x).rank().values
    ry = pd.Series(y).rank().values
    if rx.std() == 0 or ry.std() == 0: return float('nan'), len(x)
    return float(np.corrcoef(rx, ry)[0, 1]), len(x)


def main() -> None:
    DB_DIR.mkdir(parents=True, exist_ok=True)
    df = aggregate()
    print(f'Loaded {len(df)} cases.', flush=True)
    if df.empty:
        sys.exit('no cases')

    # Save raw CSV
    out_csv = DB_DIR / 'section7_fracture_aware_summary.csv'
    df.to_csv(out_csv, index=False)
    print(f'Wrote {out_csv}\n', flush=True)

    # ── 1. σ_e_loss_pct distribution (overall) ─────────────────────────
    have_loss = df['sigma_e_loss_pct'].dropna()
    print('='*78)
    print('σ_e_loss_pct distribution across 78-case ensemble')
    print('='*78)
    print(f'  n cases with loss data : {len(have_loss)}')
    print(f'  mean                    : {have_loss.mean():.2f} %')
    print(f'  median                  : {have_loss.median():.2f} %')
    print(f'  std                     : {have_loss.std():.2f} %')
    print(f'  min / max               : {have_loss.min():.2f} / {have_loss.max():.2f} %')
    print(f'  quartiles (Q1/Q2/Q3)    : '
          f'{have_loss.quantile(0.25):.2f} / {have_loss.quantile(0.5):.2f} / '
          f'{have_loss.quantile(0.75):.2f} %\n')

    # ── 2. binned distribution ───────────────────────────────────────────
    bins = [-0.001, 1, 5, 10, 25, 50, 100.001]
    labels = ['<1%', '1-5%', '5-10%', '10-25%', '25-50%', '50-100%']
    binned = pd.cut(have_loss, bins=bins, labels=labels)
    print('  binned σ_e_loss distribution:')
    for lbl, n in binned.value_counts().sort_index().items():
        print(f'    {lbl:>10s}  n = {n:3d}  ({n/len(have_loss)*100:5.1f}%)')
    print()

    # ── 3. r_SE band stratification ─────────────────────────────────────
    if df['r_SE_um'].notna().any():
        df['r_SE_band'] = pd.cut(df['r_SE_um'],
                                  bins=[0, 0.7, 1.2, 2.0],
                                  labels=['fine (<0.7μm)', 'medium (0.7-1.2)',
                                          'coarse (>1.2)'])
        print('='*78)
        print('σ_e_loss_pct stratified by r_SE band')
        print('='*78)
        for band, sub in df.groupby('r_SE_band', observed=True):
            losses = sub['sigma_e_loss_pct'].dropna()
            if len(losses) == 0: continue
            print(f'  {str(band):20s}  n={len(losses):2d}  '
                  f'mean={losses.mean():6.2f}%  median={losses.median():6.2f}%  '
                  f'max={losses.max():6.2f}%')
        print()

    # ── 4. Regressions ──────────────────────────────────────────────────
    print('='*78)
    print('Regression: predictors of σ_e_loss_pct')
    print('='*78)
    targets = [
        ('r_SE_um', 'r_SE (μm)'),
        ('ps_frac_AM_P', 'AM_P volume fraction'),
        ('frac_AM_P_AM_P_severe_pct', 'AM_P-AM_P severe %'),
        ('frac_severe_pct', 'overall severe %'),
        ('fracture_aware_excluded_pct', 'AM-AM excluded %'),
        ('porosity', 'porosity'),
    ]
    print(f'  {"predictor":35s} {"Pearson":>10s} {"Spearman":>10s} {"n":>5s}')
    print('  ' + '-' * 70)
    for col, lbl in targets:
        if col not in df.columns: continue
        r_p, n = _pearson(df[col].values, df['sigma_e_loss_pct'].values)
        r_s, _ = _spearman(df[col].values, df['sigma_e_loss_pct'].values)
        print(f'  {lbl:35s}  {r_p:>+8.3f}   {r_s:>+8.3f}   {n:>4d}')
    print()

    # ── 5. σ_e absolute values: full vs fracture-aware ──────────────────
    print('='*78)
    print('σ_e_full vs σ_e_fracture_aware — distribution')
    print('='*78)
    sf = df['sigma_e_full'].dropna()
    sfa = df['sigma_e_fracture_aware'].dropna()
    print(f'  σ_e_full           median {sf.median():.2f}  mean {sf.mean():.2f}  max {sf.max():.2f}')
    print(f'  σ_e_fracture_aware median {sfa.median():.2f}  mean {sfa.mean():.2f}  max {sfa.max():.2f}')
    if 'sigma_e_full' in df and 'sigma_e_fracture_aware' in df:
        ratios = (df['sigma_e_fracture_aware'] / df['sigma_e_full']).dropna()
        print(f'  ratio fa/full      median {ratios.median():.3f}  mean {ratios.mean():.3f}')
    print()

    # ── 6. Pareto frontier candidates (low σ_e_loss + high σ_ionic) ─────
    cands = df[(df['sigma_ionic_full'].notna())
               & (df['sigma_e_fracture_aware'].notna())].copy()
    if not cands.empty:
        cands = cands.sort_values('sigma_e_loss_pct')
        print('='*78)
        print('Top 10 cases by lowest σ_e_loss_pct (cathode-design winners)')
        print('='*78)
        cols = ['case_id', 'ps_label', 'r_SE_um', 'sigma_ionic_full',
                'sigma_e_full', 'sigma_e_fracture_aware', 'sigma_e_loss_pct',
                'frac_severe_pct', 'frac_AM_P_AM_P_severe_pct']
        print(cands[cols].head(10).to_string(index=False))
        print()
        print('Top 10 cases by highest σ_e_fracture_aware (post-fracture σ_e)')
        print('='*78)
        cands2 = cands.sort_values('sigma_e_fracture_aware', ascending=False)
        print(cands2[cols].head(10).to_string(index=False))
        print()

    # ── 7. r_SE × P:S 2D pivot for σ_e_loss ────────────────────────────
    if 'r_SE_band' in df.columns:
        df['ps_band'] = pd.cut(df['ps_frac_AM_P'].fillna(-1),
                                bins=[-1.001, 0.05, 0.4, 0.6, 0.85, 1.001],
                                labels=['0:10', '<5:5', '5:5', '>5:5', '10:0'])
        piv = df.pivot_table(values='sigma_e_loss_pct',
                              index='ps_band', columns='r_SE_band',
                              aggfunc='median', observed=True)
        print('='*78)
        print('Median σ_e_loss_pct  —  P:S band  ×  r_SE band')
        print('='*78)
        print(piv.round(2).to_string())
        print()


if __name__ == '__main__':
    main()
