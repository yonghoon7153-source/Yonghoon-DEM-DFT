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
    """Recursively find case dirs under results/ and archive/ at any depth.
    Fixes a depth-1-only iteration bug that silently skipped categorized
    archive cases (webapp/archive/category/case_id/)."""
    seen = set()
    out = []
    for base in ('results', 'archive'):
        root = WEBAPP / base
        if not root.exists():
            continue
        for fm_p in root.rglob('full_metrics.json'):
            case_dir = fm_p.parent
            if case_dir not in seen:
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


def _se_radius_from_atoms(case_dir: Path, type_map: dict, scale: float = 1000.0) -> float:
    """Return SE particle radius in REAL μm.

    atoms.csv stores radii in simulation units (meters, after scale=×1000).
    Convert to real μm: r_real_um = r_sim_m × 1e6 / scale.
    For typical scale=1000 and r_sim=5e-4 m → r_real = 0.5 μm.
    """
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
    r_sim = float(sub['radius'].median())
    # Convert sim → real μm. atoms.csv stores in meters; scale = sim/real.
    r_real_um = r_sim * 1.0e6 / scale
    return r_real_um


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


def _load_supplementary(case_id: str) -> dict:
    """Pull fracture stage metrics from b2_b4_diagnostic.csv if present."""
    sup = ROOT / 'docs' / 'figures' / 'physics_regime' / 'b2_b4_diagnostic.csv'
    if not sup.exists():
        return {}
    try:
        df = pd.read_csv(sup)
        if 'case_id' not in df.columns:
            return {}
        row = df[df['case_id'] == case_id]
        if row.empty:
            return {}
        return row.iloc[0].to_dict()
    except Exception:
        return {}


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
        scale = float(meta.get('scale', 1000))
        ps_frac, ps_label = _parse_ps_ratio(meta)
        type_map = _parse_type_map(meta.get('type_map', '1:AM_P,2:AM_S,3:SE'))
        r_SE = _se_radius_from_atoms(d, type_map, scale=scale)
        # Pull fracture metrics from supplementary CSV if not in fm
        sup = _load_supplementary(d.name)

        def pick(*keys):
            for k in keys:
                v = fm.get(k)
                if v is None:
                    v = sup.get(k)
                if v is not None and (not isinstance(v, float) or not pd.isna(v)):
                    return v
            return None
        rows.append({
            'case_id': d.name,
            'ps_label': ps_label,
            'ps_frac_AM_P': ps_frac,
            'r_SE_um': r_SE,
            'porosity': pick('porosity'),
            'percolation_pct': pick('percolation_pct', 'top_reachable_pct'),
            'sigma_ionic_full': pick('sigma_full_mScm'),
            'sigma_ionic_physics': pick('sigma_full_mScm_physics'),
            'sigma_ionic_stage_e': pick('sigma_full_mScm_stage_e'),
            'sigma_ionic_loss_pct_stage_e': pick('sigma_ionic_loss_pct_stage_e'),
            'sigma_e_full': pick('electronic_sigma_full_mScm'),
            'sigma_e_fracture_aware': pick('electronic_sigma_full_mScm_fracture_aware'),
            'sigma_e_loss_pct': pick('electronic_sigma_loss_pct'),
            'sigma_e_stagewise': pick('electronic_sigma_full_mScm_stagewise'),
            'sigma_e_loss_pct_stagewise': pick('electronic_sigma_loss_pct_stagewise'),
            'sigma_e_stage_e': pick('electronic_sigma_full_mScm_stage_e'),
            'sigma_e_loss_pct_stage_e': pick('electronic_sigma_loss_pct_stage_e'),
            'sigma_th_full': pick('thermal_sigma_full_mScm'),
            'sigma_th_fracture_aware': pick('thermal_sigma_full_mScm_fracture_aware'),
            'sigma_th_stagewise': pick('thermal_sigma_full_mScm_stagewise'),
            'sigma_th_loss_pct': pick('thermal_sigma_loss_pct'),
            'sigma_th_loss_pct_stagewise': pick('thermal_sigma_loss_pct_stagewise'),
            'sigma_th_stage_e': pick('thermal_sigma_full_mScm_stage_e'),
            'sigma_th_loss_pct_stage_e': pick('thermal_sigma_loss_pct_stage_e'),
            # Aggregated severe% — computed from individual stage keys
            # since backfill writes per-stage keys not _severe_ aggregate
            'frac_severe_pct': (
                (pick('frac_fragmentation_pct') or 0) +
                (pick('frac_pulverization_pct') or 0)
                if (pick('frac_fragmentation_pct') is not None or
                    pick('frac_pulverization_pct') is not None) else None),
            'frac_severe_force_pct': (
                (pick('frac_fragmentation_force_pct') or 0) +
                (pick('frac_pulverization_force_pct') or 0)
                if (pick('frac_fragmentation_force_pct') is not None or
                    pick('frac_pulverization_force_pct') is not None) else None),
            'frac_AM_P_AM_P_severe_pct': (
                (pick('frac_fragmentation_AM_P-AM_P_pct') or 0) +
                (pick('frac_pulverization_AM_P-AM_P_pct') or 0)
                if (pick('frac_fragmentation_AM_P-AM_P_pct') is not None or
                    pick('frac_pulverization_AM_P-AM_P_pct') is not None) else None),
            'frac_AM_P_AM_P_severe_force_pct': (
                (pick('frac_fragmentation_force_AM_P-AM_P_pct') or 0) +
                (pick('frac_pulverization_force_AM_P-AM_P_pct') or 0)
                if (pick('frac_fragmentation_force_AM_P-AM_P_pct') is not None or
                    pick('frac_pulverization_force_AM_P-AM_P_pct') is not None) else None),
            'fracture_index': pick('fracture_index'),
            'fracture_index_force': pick('fracture_index_force'),
            'n_am_am_contacts_total': pick('n_am_am_contacts_total', 'n_total_AM_AM'),
            'n_am_am_contacts_excluded': pick('n_am_am_contacts_excluded'),
            'fracture_aware_excluded_pct': pick('fracture_aware_excluded_pct'),
        })
    return pd.DataFrame(rows)


def _filter_anomalies(df: pd.DataFrame) -> pd.DataFrame:
    """Drop cases with non-physical σ values or impossible Stage-corrected ratios.

    Real cathode σ_e ∈ [0.1, 30] mS/cm; values > 100 indicate sparse-graph
    network solver numerical instability (the same g_boundary issue we
    patched for the baseline solver — Stage E's modified-contacts subprocess
    can still trip it for thin-edge graphs after σ_factor scaling).

    Anomaly criteria:
      (1) σ_e_baseline > 100 mS/cm   — baseline solver failed
      (2) σ_e Stage-C > 100          — fracture-aware solver failed
      (3) σ_e_loss_pct out of [-5, 100]  — non-physical loss%
      (4) σ_e_stage_e > 5× baseline      — Stage E inflation bug
                                            (Stage E should reduce σ_e via
                                             σ_factor ≤ 1 and grain factor
                                             ≤ 1; ratio >5 means subprocess
                                             ill-conditioned for this case's
                                             modified-contact topology)
      (5) σ_th_stage_e > 5× baseline     — same Stage E bug for κ
    """
    n0 = len(df)
    df = df[(df['sigma_e_full'].fillna(0) < 100) &
             (df['sigma_e_full'].fillna(0) >= 0)]
    df = df[(df['sigma_e_fracture_aware'].fillna(0) < 100) &
             (df['sigma_e_fracture_aware'].fillna(0) >= 0)]
    df = df[(df['sigma_e_loss_pct'].fillna(0) >= -5) &
             (df['sigma_e_loss_pct'].fillna(0) <= 100)]

    # Stage E inflation safety net (kept as defence-in-depth — the
    # underlying g_boundary issue was fixed in network_conductivity.py
    # commit-pending, so this filter should now drop 0 cases on a fresh
    # rerun). Threshold 5× catches any residual numerical artifacts.
    if 'sigma_e_stage_e' in df.columns and 'sigma_e_full' in df.columns:
        ratio_e = df['sigma_e_stage_e'] / df['sigma_e_full'].replace(0, float('nan'))
        bad_e = ratio_e.fillna(0) > 5.0
        df = df[~bad_e]
    if 'sigma_th_stage_e' in df.columns and 'sigma_th_full' in df.columns:
        ratio_th = df['sigma_th_stage_e'] / df['sigma_th_full'].replace(0, float('nan'))
        bad_th = ratio_th.fillna(0) > 5.0
        df = df[~bad_th]

    print(f'  filtered {n0} → {len(df)} cases (removed {n0-len(df)} anomalies)\n',
          flush=True)
    return df.reset_index(drop=True)


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
    df_raw = aggregate()
    print(f'Loaded {len(df_raw)} cases (raw).', flush=True)
    if df_raw.empty:
        sys.exit('no cases')

    # Save raw CSV (all 78 cases including anomalies)
    out_csv = DB_DIR / 'section7_fracture_aware_summary.csv'
    df_raw.to_csv(out_csv, index=False)
    print(f'Wrote {out_csv}', flush=True)

    # Anomaly-filtered analysis frame
    df = _filter_anomalies(df_raw)
    if df.empty:
        sys.exit('no cases after anomaly filter')
    df.to_csv(DB_DIR / 'section7_fracture_aware_filtered.csv', index=False)

    # r_SE distribution sanity check
    print('r_SE distribution (μm):', flush=True)
    print(f'  unique values: {sorted(df["r_SE_um"].dropna().unique())[:10]}')
    print(f'  median {df["r_SE_um"].median():.2f} μm  '
          f'min {df["r_SE_um"].min():.2f}  max {df["r_SE_um"].max():.2f}\n')

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

    # ── 5. σ_e absolute values: full vs fracture-aware (binary) vs stagewise ────
    print('='*78)
    print('σ_e: full vs fracture-aware (binary) vs stagewise (Lawn-Lit)')
    print('='*78)
    sf = df['sigma_e_full'].dropna()
    sfa = df['sigma_e_fracture_aware'].dropna()
    ssw = df['sigma_e_stagewise'].dropna() if 'sigma_e_stagewise' in df.columns else pd.Series(dtype=float)
    print(f'  σ_e_full           median {sf.median():6.2f}  mean {sf.mean():6.2f}  max {sf.max():6.2f}  n={len(sf)}')
    print(f'  σ_e binary  (R=∞)  median {sfa.median():6.2f}  mean {sfa.mean():6.2f}  max {sfa.max():6.2f}  n={len(sfa)}')
    if len(ssw):
        print(f'  σ_e stagewise      median {ssw.median():6.2f}  mean {ssw.mean():6.2f}  max {ssw.max():6.2f}  n={len(ssw)}')
    if 'sigma_e_fracture_aware' in df:
        ratios = (df['sigma_e_fracture_aware'] / df['sigma_e_full']).dropna()
        print(f'  binary  fa/full    median {ratios.median():.3f}  mean {ratios.mean():.3f}')
    if 'sigma_e_stagewise' in df.columns:
        ratios_sw = (df['sigma_e_stagewise'] / df['sigma_e_full']).dropna()
        if len(ratios_sw):
            print(f'  stagewise sw/full  median {ratios_sw.median():.3f}  mean {ratios_sw.mean():.3f}')
    print()
    if 'sigma_e_loss_pct_stagewise' in df.columns:
        sw_loss = df['sigma_e_loss_pct_stagewise'].dropna()
        if len(sw_loss):
            print('  Stagewise loss_pct distribution:')
            print(f'    n {len(sw_loss)}  mean {sw_loss.mean():.2f}%  median {sw_loss.median():.2f}%  '
                  f'Q1/Q3 {sw_loss.quantile(0.25):.2f} / {sw_loss.quantile(0.75):.2f}%')
            print()

    # ── 5b. Stage E (full literature-grounded) results ──────────────────────
    print('='*78)
    print('Stage E (literature-grounded full corrections) — all 3 channels')
    print('='*78)
    if 'sigma_ionic_stage_e' in df.columns:
        si_full = df['sigma_ionic_full'].dropna()
        si_e    = df['sigma_ionic_stage_e'].dropna()
        si_loss = df['sigma_ionic_loss_pct_stage_e'].dropna() if 'sigma_ionic_loss_pct_stage_e' in df.columns else pd.Series(dtype=float)
        print(f'  σ_ionic baseline   median {si_full.median():6.4f}  n={len(si_full)}')
        print(f'  σ_ionic Stage E    median {si_e.median():6.4f}  n={len(si_e)}')
        if len(si_loss):
            print(f'  σ_ionic loss%      mean {si_loss.mean():6.2f}%  median {si_loss.median():6.2f}%  '
                  f'Q3 {si_loss.quantile(0.75):.2f}%')
        print()
    if 'sigma_e_stage_e' in df.columns:
        se_e_e  = df['sigma_e_stage_e'].dropna()
        se_loss = df['sigma_e_loss_pct_stage_e'].dropna() if 'sigma_e_loss_pct_stage_e' in df.columns else pd.Series(dtype=float)
        print(f'  σ_e baseline       median {df["sigma_e_full"].dropna().median():6.2f}  n={len(df["sigma_e_full"].dropna())}')
        print(f'  σ_e Stage E        median {se_e_e.median():6.2f}  mean {se_e_e.mean():6.2f}  max {se_e_e.max():6.2f}  n={len(se_e_e)}')
        if len(se_loss):
            print(f'  σ_e Stage E loss%  mean {se_loss.mean():6.2f}%  median {se_loss.median():6.2f}%  '
                  f'Q1/Q3 {se_loss.quantile(0.25):.2f} / {se_loss.quantile(0.75):.2f}%')
        ratios_e = (df['sigma_e_stage_e'] / df['sigma_e_full']).dropna()
        if len(ratios_e):
            print(f'  σ_e fa(E)/full     median {ratios_e.median():.3f}  mean {ratios_e.mean():.3f}')
        print()
    if 'sigma_th_stage_e' in df.columns:
        sth_full = df['sigma_th_full'].dropna()
        sth_e    = df['sigma_th_stage_e'].dropna()
        sth_loss = df['sigma_th_loss_pct_stage_e'].dropna() if 'sigma_th_loss_pct_stage_e' in df.columns else pd.Series(dtype=float)
        print(f'  κ baseline         median {sth_full.median():6.2f}  n={len(sth_full)}')
        print(f'  κ Stage E          median {sth_e.median():6.2f}  mean {sth_e.mean():6.2f}  n={len(sth_e)}')
        if len(sth_loss):
            print(f'  κ Stage E loss%    mean {sth_loss.mean():6.2f}%  median {sth_loss.median():6.2f}%  '
                  f'Q1/Q3 {sth_loss.quantile(0.25):.2f} / {sth_loss.quantile(0.75):.2f}%')
        ratios_th = (df['sigma_th_stage_e'] / df['sigma_th_full']).dropna()
        if len(ratios_th):
            print(f'  κ E/full           median {ratios_th.median():.3f}  mean {ratios_th.mean():.3f}')
        print()

    # ── 5c. r_SE band stratification for Stage E σ_e_loss ────────────────
    if 'sigma_e_loss_pct_stage_e' in df.columns and 'r_SE_band' in df.columns:
        print('='*78)
        print('Stage E σ_e loss% stratified by r_SE band')
        print('='*78)
        for band, sub in df.groupby('r_SE_band', observed=True):
            losses = sub['sigma_e_loss_pct_stage_e'].dropna()
            if len(losses) == 0: continue
            print(f'  {str(band):20s}  n={len(losses):2d}  '
                  f'mean={losses.mean():6.2f}%  median={losses.median():6.2f}%  '
                  f'max={losses.max():6.2f}%')
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

    # ── 6b. Pareto winners by Stage E (literature-realistic) ────────────
    if 'sigma_e_stage_e' in df.columns:
        cands_e = df[(df['sigma_ionic_full'].notna())
                      & (df['sigma_e_stage_e'].notna())].copy()
        if not cands_e.empty:
            cols_e = ['case_id', 'ps_label', 'r_SE_um', 'sigma_ionic_full',
                       'sigma_e_full', 'sigma_e_stage_e', 'sigma_e_loss_pct_stage_e',
                       'sigma_th_stage_e', 'sigma_th_loss_pct_stage_e']
            print('='*78)
            print('Stage E Top 10 — lowest σ_e loss (literature-realistic winners)')
            print('='*78)
            cands_e_low = cands_e.sort_values('sigma_e_loss_pct_stage_e')
            print(cands_e_low[cols_e].head(10).to_string(index=False))
            print()
            print('Stage E Top 10 — highest σ_e_stage_e (post-correction σ_e value)')
            print('='*78)
            cands_e_high = cands_e.sort_values('sigma_e_stage_e', ascending=False)
            print(cands_e_high[cols_e].head(10).to_string(index=False))
            print()
            # 3-objective Pareto: σ_ionic high + σ_e_stage_e high + κ_stage_e high
            print('Stage E Top 10 — composite Pareto rank (σ_ionic+σ_e+κ all post-correction)')
            print('='*78)
            tmp = cands_e.copy()
            for c in ['sigma_ionic_full', 'sigma_e_stage_e', 'sigma_th_stage_e']:
                if c in tmp.columns:
                    mn, mx = tmp[c].min(), tmp[c].max()
                    rng = mx - mn if mx > mn else 1
                    tmp[f'{c}_norm'] = (tmp[c] - mn) / rng
            score_cols = [f'{c}_norm' for c in
                           ['sigma_ionic_full', 'sigma_e_stage_e', 'sigma_th_stage_e']
                           if f'{c}_norm' in tmp.columns]
            if score_cols:
                tmp['pareto_score'] = tmp[score_cols].mean(axis=1)
                tmp_sorted = tmp.sort_values('pareto_score', ascending=False)
                print(tmp_sorted[cols_e + ['pareto_score']].head(10).to_string(index=False))
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
