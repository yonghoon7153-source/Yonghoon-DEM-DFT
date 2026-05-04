#!/usr/bin/env python3
"""Build / update the master metrics DB.

Aggregates per-case full_metrics.json (+ meta.json, input_params.json,
supplementary CSVs in docs/figures/physics_regime/) into one flat
DataFrame with a single row per case.

Output (docs/db/):
  metrics_master.csv         — flat table, primary artifact for analysis
  metrics_master.sqlite      — same data SQL-queryable
  .mtime_cache.json          — per-case mtime, used to skip unchanged cases
  snapshots/<tag>.csv        — tagged frozen copies (for before/after diff)

Usage:
  python3 scripts/build_metrics_db.py                       # incremental update
  python3 scripts/build_metrics_db.py --rebuild             # full rebuild
  python3 scripts/build_metrics_db.py --snapshot pre_tier1  # tag current state
  python3 scripts/build_metrics_db.py --diff a b            # column-level diff
  python3 scripts/build_metrics_db.py --list-snapshots
  python3 scripts/build_metrics_db.py --columns             # show column groups

Pipeline integration:
  • Stage A (re-analysis) → run this with --snapshot post_tier1
  • Then --diff pre_tier1 post_tier1 to see what changed
  • New supplementary CSVs (b2_b4_diagnostic, tau_3way, ...) are auto-
    merged on case_id with their filename as prefix.
"""
from __future__ import annotations
import argparse
import json
import sqlite3
import sys
from pathlib import Path
from datetime import datetime

import pandas as pd
import numpy as np


ROOT = Path(__file__).resolve().parent.parent
WEBAPP = ROOT / 'webapp'
DB_DIR = ROOT / 'docs' / 'db'
SNAPSHOT_DIR = DB_DIR / 'snapshots'
SUP_DIR = ROOT / 'docs' / 'figures' / 'physics_regime'

MASTER_CSV    = DB_DIR / 'metrics_master.csv'
MASTER_SQLITE = DB_DIR / 'metrics_master.sqlite'
CACHE_FILE    = DB_DIR / '.mtime_cache.json'


# ── Column groups (for --columns inspection / docs) ───────────────────────
COLUMN_GROUPS: dict[str, list[str]] = {
    'identity':    ['case_id', 'name', 'batch', 'last_updated_iso'],
    'geometry':    ['porosity', 'phi_se', 'thickness_um', 'plate_z_source',
                    'ps_ratio', 'am_se_ratio'],
    'tortuosity':  ['tortuosity_mean', 'tortuosity_median',
                    'tortuosity_recommended', 'tortuosity_use_median',
                    'tau_dij_R', 'tau_lap_eff'],
    'percolation': ['percolation_pct', 'top_reachable_pct',
                    'n_components', 'n_large_components'],
    'cn_se_se':    ['se_se_cn', 'se_se_cn_std',
                    # F2: percolating-only + area-weighted (post tier1)
                    'se_se_cn_perc', 'se_se_cn_eff_area',
                    'se_se_cn_eff_area_perc', 'se_se_cn_n_perc',
                    # F1: plastic-augmented (post tier1)
                    'se_se_cn_aug', 'se_se_cn_aug_n_extra',
                    'se_se_cn_aug_h_spread_sim'],
    'cn_am':       ['am_am_cn', 'am_se_cn_mean', 'am_se_cn_surface_weighted'],
    'coverage':    ['coverage_AM_S_mean', 'coverage_AM_P_mean',
                    'coverage_AM_S_mean_physics', 'coverage_AM_P_mean_physics',
                    'coverage_AM_S_mean_physics_rough',  # B3 post tier1
                    'coverage_AM_P_mean_physics_rough',
                    'coverage_AM_mean_physics_rough'],
    'sigma':       ['sigma', 'sigma_full_H', 'sigma_bulk_H', 'sigma_constr_H',
                    'sigma_P', 'sigma_H'],
    'gb':          ['gb_density_mean', 'gb_density_median', 'gb_density_p95'],
    'pressure':    ['stack_pressure_MPa'],
    'patch_flags': ['patch_C4_applied', 'patch_F1_h_spread_sim',
                    'patch_F2_applied', 'patch_B3_applied',
                    'sigma_model'],
}


# ── Helpers ───────────────────────────────────────────────────────────────

def _load_json(path: Path) -> dict | None:
    if not path.exists():
        return None
    try:
        return json.load(open(path))
    except Exception:
        return None


def detect_batch(name: str | None) -> str:
    if not name:
        return 'unknown'
    n = str(name).lower()
    for tag in ('1mah', '6mah', '8mah'):
        if tag in n:
            return tag.replace('mah', 'mAh')
    if 'particulate' in n:
        return 'particulate'
    return 'other'


def _flatten(prefix: str, obj, out: dict, max_depth: int = 2) -> None:
    """Flatten nested dict/scalar into out dict using __ as separator."""
    if isinstance(obj, dict):
        if max_depth <= 0:
            return
        for k, v in obj.items():
            _flatten(f'{prefix}__{k}' if prefix else str(k), v, out, max_depth - 1)
    elif isinstance(obj, (int, float, str, bool, type(None))):
        out[prefix] = obj
    # arrays / lists: skipped (rows must be scalar)


def case_to_row(case_dir: Path) -> dict | None:
    """Convert a single case directory into one flat row dict."""
    fm_path = case_dir / 'full_metrics.json'
    fm = _load_json(fm_path)
    if fm is None:
        return None

    # meta.json sometimes lives under the case dir, sometimes under
    # webapp/uploads/<case_id>/. Try both.
    meta = _load_json(case_dir / 'meta.json') or \
           _load_json(WEBAPP / 'uploads' / case_dir.name / 'meta.json') or {}
    params = _load_json(case_dir / 'input_params.json') or {}

    row: dict = {
        'case_id': case_dir.name,
        'name':    meta.get('name', case_dir.name),
        'batch':   detect_batch(meta.get('name', '')),
        'last_updated_iso': datetime.fromtimestamp(
            fm_path.stat().st_mtime).isoformat(timespec='seconds'),
        'last_updated_ts':  fm_path.stat().st_mtime,
        'case_path':        str(case_dir.relative_to(ROOT)),
    }

    # Flatten full_metrics.json (one level of nested dicts allowed)
    _flatten('', fm, row, max_depth=2)

    # Stack pressure (try multiple key conventions)
    p_mpa = params.get('stack_pressure_MPa')
    if p_mpa is None:
        p_pa = params.get('stack_pressure_pa') or params.get('stack_pressure_Pa')
        if p_pa:
            try:
                p_mpa = float(p_pa) / 1e6
            except Exception:
                p_mpa = None
    if p_mpa is None:
        p_mpa = params.get('pressure_MPa') or params.get('P_MPa')
    row['stack_pressure_MPa'] = p_mpa

    # Patch-detection flags — derived from key presence
    row['patch_F1_h_spread_sim']  = fm.get('se_se_cn_aug_h_spread_sim')
    row['patch_F2_applied']       = ('se_se_cn_perc' in fm
                                      and fm.get('se_se_cn_perc') is not None)
    row['patch_B3_applied']       = ('coverage_AM_mean_physics_rough' in fm)
    # patch_C4_applied: hard to detect from output alone (boundary changes
    # affect percolation_pct but no flag is written). Default to None.
    row['patch_C4_applied']       = None
    row['sigma_model']            = fm.get('sigma_model', 'uniform')

    return row


def discover_cases() -> list[Path]:
    """Recursively find case dirs at any depth under results/ or archive/."""
    seen = set()
    out = []
    for base in ('results', 'archive'):
        root = WEBAPP / base
        if root.exists():
            for fm_p in root.rglob('full_metrics.json'):
                case_dir = fm_p.parent
                if case_dir not in seen:
                    seen.add(case_dir)
                    out.append(case_dir)
    return sorted(out)


def load_cache() -> dict:
    if CACHE_FILE.exists():
        return _load_json(CACHE_FILE) or {}
    return {}


def save_cache(cache: dict) -> None:
    CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
    json.dump(cache, open(CACHE_FILE, 'w'), indent=2)


def merge_supplementary(df: pd.DataFrame) -> pd.DataFrame:
    """Auto-merge any case-id-keyed CSV in SUP_DIR using filename as prefix."""
    if not SUP_DIR.exists():
        return df
    for csv_path in sorted(SUP_DIR.glob('*.csv')):
        try:
            sup = pd.read_csv(csv_path)
        except Exception as e:
            print(f'  [warn] {csv_path.name}: read failed ({e})')
            continue
        # Identify case-id column
        cid_col = None
        for c in ('case_id', 'case', 'cid', 'id'):
            if c in sup.columns:
                cid_col = c
                break
        if cid_col is None:
            continue  # not a case-keyed table
        if cid_col != 'case_id':
            sup = sup.rename(columns={cid_col: 'case_id'})

        # Drop columns that already exist in master to avoid _x/_y collisions.
        for redundant in ('name', 'batch'):
            if redundant in sup.columns:
                sup = sup.drop(columns=[redundant])

        # Some supplementary tables (e.g. coverage_hertz_vs_physics_summary
        # carries one row per (case_id, am_type)) have multiple rows per
        # case_id. A naive left-merge then explodes the master row count.
        # Aggregate to one row per case_id by averaging numeric columns and
        # joining string columns with '|' so the merge stays 1:1.
        if sup['case_id'].duplicated().any():
            n_before = len(sup)
            agg_funcs = {}
            for c in sup.columns:
                if c == 'case_id': continue
                if pd.api.types.is_numeric_dtype(sup[c]):
                    agg_funcs[c] = 'mean'
                else:
                    agg_funcs[c] = lambda s: '|'.join(
                        sorted(set(str(v) for v in s.dropna())))
            sup = sup.groupby('case_id', as_index=False).agg(agg_funcs)
            print(f'  [info] {csv_path.name}: aggregated {n_before} rows '
                  f'→ {len(sup)} rows (one per case)')

        # Prefix all remaining non-case columns with the source filename.
        prefix = csv_path.stem + '__'
        rename = {c: prefix + c for c in sup.columns if c != 'case_id'}
        sup = sup.rename(columns=rename)

        # Defensive: if any prefixed column would still clash with the
        # master, keep the master copy (drop from sup).
        clashes = [c for c in sup.columns
                   if c != 'case_id' and c in df.columns]
        if clashes:
            print(f'  [warn] {csv_path.name}: dropping clashing columns '
                  f'{clashes}')
            sup = sup.drop(columns=clashes)

        before_cols = len(df.columns)
        df = df.merge(sup, on='case_id', how='left')
        added = len(df.columns) - before_cols
        if added:
            print(f'  + {csv_path.name}: merged {added} columns '
                  f'(prefix "{prefix}")')
    return df


def build_master(force: bool = False) -> pd.DataFrame:
    """Scan all case dirs and build the master DataFrame.

    When `force=False`, cases whose full_metrics.json mtime hasn't changed
    since last run are skipped — but we still need to load the previous
    master CSV to keep their rows. This is the "incremental" mode.
    """
    cases = discover_cases()
    print(f'Found {len(cases)} case directories.', flush=True)

    cache = load_cache() if not force else {}
    new_cache = {}

    # Load previous master (if any) for incremental
    prev_df: pd.DataFrame | None = None
    if not force and MASTER_CSV.exists():
        try:
            prev_df = pd.read_csv(MASTER_CSV)
            print(f'  prev master: {len(prev_df)} rows × {len(prev_df.columns)} cols',
                  flush=True)
        except Exception:
            prev_df = None

    rows = []
    n_recomputed = 0
    n_reused = 0
    for cd in cases:
        fm_path = cd / 'full_metrics.json'
        mtime = fm_path.stat().st_mtime
        new_cache[cd.name] = mtime

        # Try to reuse from prev_df if mtime unchanged
        if (prev_df is not None
                and not force
                and cache.get(cd.name) == mtime
                and (prev_df['case_id'] == cd.name).any()):
            row = prev_df[prev_df['case_id'] == cd.name].iloc[0].to_dict()
            n_reused += 1
        else:
            row = case_to_row(cd)
            if row is None:
                continue
            n_recomputed += 1
        rows.append(row)

    print(f'  recomputed: {n_recomputed}, reused: {n_reused}', flush=True)

    df = pd.DataFrame(rows)

    # Supplementary CSVs (b2_b4_diagnostic, tau_3way, coverage_summary, ...)
    df = merge_supplementary(df)

    # Outputs
    DB_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(MASTER_CSV, index=False)
    try:
        # SQLite — column names with __ might confuse some readers but it's
        # sqlite3 default behaviour to quote them.
        conn = sqlite3.connect(MASTER_SQLITE)
        df.to_sql('metrics', conn, if_exists='replace', index=False)
        conn.close()
    except Exception as e:
        print(f'  [warn] SQLite write failed: {e}', flush=True)
    save_cache(new_cache)

    print(f'→ {MASTER_CSV.relative_to(ROOT)}  '
          f'({len(df)} cases × {len(df.columns)} columns)', flush=True)
    return df


def save_snapshot(tag: str, df: pd.DataFrame | None = None) -> Path:
    """Freeze current master as a snapshot under docs/db/snapshots/<tag>.csv."""
    if df is None:
        if not MASTER_CSV.exists():
            df = build_master()
        else:
            df = pd.read_csv(MASTER_CSV)
    SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)
    out = SNAPSHOT_DIR / f'{tag}.csv'
    df.to_csv(out, index=False)
    print(f'→ Snapshot "{tag}": {out.relative_to(ROOT)}  '
          f'({len(df)} rows × {len(df.columns)} cols)', flush=True)
    return out


def list_snapshots() -> list[str]:
    if not SNAPSHOT_DIR.exists():
        return []
    out = []
    for p in sorted(SNAPSHOT_DIR.glob('*.csv')):
        ts = datetime.fromtimestamp(p.stat().st_mtime).isoformat(timespec='seconds')
        try:
            n = sum(1 for _ in open(p)) - 1
        except Exception:
            n = -1
        out.append((p.stem, ts, n))
        print(f'  {p.stem:30s}  {ts}  ({n} rows)')
    return out


def diff_snapshots(tag1: str, tag2: str, n_top: int = 30) -> pd.DataFrame:
    """Report column-level changes between two snapshots."""
    f1 = SNAPSHOT_DIR / f'{tag1}.csv'
    f2 = SNAPSHOT_DIR / f'{tag2}.csv'
    if not f1.exists():
        sys.exit(f'Snapshot not found: {f1}')
    if not f2.exists():
        sys.exit(f'Snapshot not found: {f2}')
    df1 = pd.read_csv(f1)
    df2 = pd.read_csv(f2)

    only1 = sorted(set(df1.columns) - set(df2.columns))
    only2 = sorted(set(df2.columns) - set(df1.columns))
    common = sorted(set(df1.columns) & set(df2.columns))
    common = [c for c in common if c not in
              ('case_id', 'name', 'batch', 'case_path',
               'last_updated_iso', 'last_updated_ts')]

    print(f'\n=== Diff "{tag1}" → "{tag2}" ===', flush=True)
    if only1:
        print(f'  columns only in {tag1}: {only1}', flush=True)
    if only2:
        print(f'  columns only in {tag2}: {only2}', flush=True)

    df1m = df1.set_index('case_id')
    df2m = df2.set_index('case_id')
    common_cases = sorted(set(df1m.index) & set(df2m.index))
    print(f'  {len(common_cases)} cases in both snapshots\n', flush=True)

    diffs = []
    for col in common:
        try:
            # Force numeric conversion — boolean / string columns become NaN
            v1 = pd.to_numeric(df1m.loc[common_cases, col], errors='coerce')
            v2 = pd.to_numeric(df2m.loc[common_cases, col], errors='coerce')
        except KeyError:
            continue
        # Skip non-numeric or all-missing columns
        if v1.dtype == object or v2.dtype == object: continue
        if v1.isna().all() or v2.isna().all():
            continue
        # Per-row absolute diff (cast to float to dodge any boolean dtype quirks)
        d = (v2.astype(float) - v1.astype(float)).abs()
        n_changed = int((d > max(1e-9, 1e-6 * v1.abs().mean())).sum())
        if n_changed == 0:
            continue
        m1 = float(v1.mean(skipna=True))
        m2 = float(v2.mean(skipna=True))
        pct = ((m2 - m1) / m1 * 100) if m1 not in (0, None) and not np.isnan(m1) else float('nan')
        diffs.append({
            'column': col,
            'n_changed': n_changed,
            f'mean_{tag1}': round(m1, 6),
            f'mean_{tag2}': round(m2, 6),
            'pct_change_mean': round(pct, 3),
        })

    diff_df = pd.DataFrame(diffs)
    if diff_df.empty:
        print('  (no numeric column-level differences)', flush=True)
        return diff_df
    diff_df = diff_df.sort_values('pct_change_mean',
                                  key=lambda s: s.abs(),
                                  ascending=False)
    print(diff_df.head(n_top).to_string(index=False))
    print(f'\n  ({len(diff_df)} columns changed; showing top {min(n_top, len(diff_df))} by |Δ%|)',
          flush=True)
    return diff_df


def show_columns(df: pd.DataFrame | None = None) -> None:
    if df is None and MASTER_CSV.exists():
        df = pd.read_csv(MASTER_CSV, nrows=1)
    cols = set(df.columns) if df is not None else set()
    print('\n=== Column groups ===\n', flush=True)
    grouped = set()
    for grp, names in COLUMN_GROUPS.items():
        present = [n for n in names if n in cols]
        missing = [n for n in names if n not in cols]
        print(f'[{grp}]  ({len(present)}/{len(names)} present)')
        for n in names:
            tag = '✓' if n in cols else '·'
            print(f'    {tag}  {n}')
            grouped.add(n)
        print()
    other = sorted(cols - grouped)
    if other:
        print(f'[other]  ({len(other)} columns not in declared groups)')
        for n in other[:30]:
            print(f'    -  {n}')
        if len(other) > 30:
            print(f'    ... and {len(other) - 30} more')


def main() -> None:
    ap = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                  description=__doc__)
    ap.add_argument('--rebuild', action='store_true',
                    help='Force full rebuild (ignore mtime cache)')
    ap.add_argument('--snapshot', metavar='TAG', default=None,
                    help='Save current master as a tagged snapshot')
    ap.add_argument('--diff', nargs=2, metavar=('TAG1', 'TAG2'), default=None,
                    help='Diff two snapshots column-by-column')
    ap.add_argument('--list-snapshots', action='store_true',
                    help='List existing snapshots')
    ap.add_argument('--columns', action='store_true',
                    help='Show column groups present / missing')
    ap.add_argument('--top', type=int, default=30,
                    help='Top-N rows to show in --diff (default 30)')
    args = ap.parse_args()

    if args.list_snapshots:
        list_snapshots()
        return
    if args.diff:
        diff_snapshots(args.diff[0], args.diff[1], n_top=args.top)
        return
    if args.columns:
        show_columns()
        return

    df = build_master(force=args.rebuild)
    if args.snapshot:
        save_snapshot(args.snapshot, df)


if __name__ == '__main__':
    main()
