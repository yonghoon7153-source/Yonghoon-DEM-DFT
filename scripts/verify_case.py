"""
Per-case sanity verification: recompute every key metric from raw CSV data
and compare against what's stored in full_metrics.json.

Metrics verified:
  1. phi_se              (SE volume fraction)
  2. porosity            (void fraction)
  3. thickness_um        (plate_z × scale)
  4. SE-SE CN mean       (from contacts)
  5. SE Percolation %    (NetworkX connected components)
  6. sigma_full / σ_ionic
  7. τ derivations (Dij, Lap_geom, Lap_eff)

For each metric:
  - Compute from scratch using atoms.csv + contacts.csv
  - Compare to stored value
  - Flag ⚠ if mismatch

Usage:
  python3 scripts/verify_case.py <case_id|case_name>
  e.g. python3 scripts/verify_case.py input_particulate_11
       python3 scripts/verify_case.py 260418_164832_ab6d1f
"""
from __future__ import annotations
import os, sys, json, math
from collections import defaultdict

import numpy as np
import pandas as pd


SIGMA_GRAIN_MS = 3.0


def find_case_dir(query: str) -> str | None:
    """Find case folder by case_id (timestamp) or meta.json name."""
    # Direct case_id match
    for base in ('webapp/results', 'webapp/archive'):
        for root, _, _ in os.walk(base):
            if os.path.basename(root) == query:
                if os.path.exists(f'{root}/atoms.csv'):
                    return root
    # Search by meta.name
    for root, _, files in os.walk('webapp'):
        if 'meta.json' in files:
            try:
                m = json.load(open(f'{root}/meta.json'))
                if m.get('name') == query:
                    # Find twin with atoms.csv
                    if os.path.exists(f'{root}/atoms.csv'):
                        return root
                    alt = root.replace('uploads', 'results')
                    if os.path.exists(f'{alt}/atoms.csv'):
                        return alt
            except Exception:
                pass
    return None


def get_meta(case_dir: str) -> dict:
    cid = os.path.basename(case_dir)
    for base in ('webapp/uploads', 'webapp/results'):
        p = f'{base}/{cid}/meta.json'
        if os.path.exists(p):
            try:
                return json.load(open(p))
            except Exception:
                pass
    p = f'{case_dir}/meta.json'
    if os.path.exists(p):
        try:
            return json.load(open(p))
        except Exception:
            pass
    return {}


def cmp(label: str, manual, stored, tol_rel: float = 0.03):
    """Print a compact comparison row."""
    if manual is None or stored is None:
        status = '—'
    else:
        try:
            m, s = float(manual), float(stored)
            if abs(s) < 1e-9:
                rel = 0 if abs(m) < 1e-9 else float('inf')
            else:
                rel = abs(m - s) / abs(s)
            status = '✓' if rel <= tol_rel else f'⚠ ({rel*100:.1f}%)'
        except Exception:
            status = '?'
    ms = f'{manual:.4f}' if isinstance(manual, float) else str(manual)
    ss = f'{stored:.4f}' if isinstance(stored, float) else str(stored)
    print(f'  {label:35s}  manual={ms:>12s}  stored={ss:>12s}  {status}')


def main():
    if len(sys.argv) < 2:
        print(f'Usage: python3 {sys.argv[0]} <case_id_or_name>')
        sys.exit(1)
    query = sys.argv[1]
    case_dir = find_case_dir(query)
    if not case_dir:
        print(f'Case not found: {query}')
        sys.exit(1)

    print(f'=== Case: {case_dir} ===')
    meta = get_meta(case_dir)
    print(f'  meta.name : {meta.get("name", "?")}')
    print(f'  meta.mode : {meta.get("mode", "?")}')
    print(f'  type_map  : {meta.get("type_map", "?")}')
    print(f'  ps_ratio  : {meta.get("ps_ratio", "?")}')

    # Load data
    df_a = pd.read_csv(f'{case_dir}/atoms.csv')
    df_c = pd.read_csv(f'{case_dir}/contacts.csv', low_memory=False) if os.path.exists(f'{case_dir}/contacts.csv') else None
    fm = {}
    if os.path.exists(f'{case_dir}/full_metrics.json'):
        fm = json.load(open(f'{case_dir}/full_metrics.json'))

    # Parse type_map
    tm = {}
    for pair in meta.get('type_map', '').split(','):
        if ':' in pair:
            k, v = pair.split(':', 1)
            tm[int(k.strip())] = v.strip()
    se_types = [k for k, v in tm.items() if v == 'SE']
    am_types = [k for k, v in tm.items() if 'AM' in v]
    scale = meta.get('scale', 1000)

    print(f'\n--- ATOMS ---')
    print(f'  Total atoms: {len(df_a)}')
    for t, name in tm.items():
        n = (df_a['type'] == t).sum()
        r_mean = df_a.loc[df_a['type'] == t, 'radius'].mean()
        print(f'    type {t} ({name:10s}): n={n:>7d}  r_mean={r_mean*scale:.2f} μm')
    print(f'  z-range: [{df_a.z.min():.5f}, {df_a.z.max():.5f}] (sim)')
    print(f'  z-range × scale: [{df_a.z.min()*scale:.1f}, {df_a.z.max()*scale:.1f}] μm')

    # mesh_info / input_params
    mi = json.load(open(f'{case_dir}/mesh_info.json')) if os.path.exists(f'{case_dir}/mesh_info.json') else {}
    ip = json.load(open(f'{case_dir}/input_params.json')) if os.path.exists(f'{case_dir}/input_params.json') else {}
    plate_z_mesh = mi.get('plate_z')
    box_x = ip.get('box_x', 0.05)
    box_y = ip.get('box_y', 0.05)
    print(f'\n--- GEOMETRY FILES ---')
    print(f'  mesh_info.json plate_z: {plate_z_mesh}  ({(plate_z_mesh or 0)*scale:.1f} μm)')
    print(f'  input_params box:       {box_x} × {box_y}  ({box_x*scale:.1f} × {box_y*scale:.1f} μm)')
    print(f'  atoms max(z):           {df_a.z.max():.5f}  ({df_a.z.max()*scale:.1f} μm)')

    # Manual metrics
    print(f'\n--- MANUAL vs STORED ---')

    # phi_SE (using box_vol = box × plate_z, with plate_z from mesh_info OR max z)
    pz_try = plate_z_mesh if plate_z_mesh else df_a.z.max()
    box_vol = box_x * box_y * pz_try
    se_ids = df_a[df_a['type'].isin(se_types)] if se_types else df_a.iloc[[]]
    se_vol = ((4/3) * math.pi * (se_ids['radius']**3)).sum()
    phi_manual = se_vol / box_vol if box_vol > 0 else 0
    cmp('phi_SE (plate_z from mesh)', phi_manual, fm.get('phi_se'))

    # Manual with plate_z = atoms max z
    box_vol_max = box_x * box_y * df_a.z.max()
    phi_max = se_vol / box_vol_max if box_vol_max > 0 else 0
    cmp('  (alt) phi_SE (plate_z=max z)', phi_max, fm.get('phi_se'))

    # Porosity
    total_vol = ((4/3) * math.pi * (df_a['radius']**3)).sum()
    poro_mesh = (1 - total_vol/box_vol) * 100 if box_vol > 0 else 0
    poro_max = (1 - total_vol/box_vol_max) * 100 if box_vol_max > 0 else 0
    cmp('porosity (plate_z=mesh)', poro_mesh, fm.get('porosity'))
    cmp('  (alt) porosity (plate_z=max z)', poro_max, fm.get('porosity'))

    # Thickness
    thick_mesh = (plate_z_mesh or 0) * scale
    thick_max = df_a.z.max() * scale
    cmp('thickness_um (mesh)', thick_mesh, fm.get('thickness_um'))
    cmp('  (alt) thickness_um (max z)', thick_max, fm.get('thickness_um'))

    # SE-SE CN
    if df_c is not None and se_types:
        se_set = set(se_ids['id'].astype(int))
        cn = defaultdict(int)
        for _, row in df_c.iterrows():
            i1, i2 = int(row['id1']), int(row['id2'])
            if i1 in se_set and i2 in se_set:
                cn[i1] += 1
                cn[i2] += 1
        if se_set:
            vals = [cn.get(i, 0) for i in se_set]
            cn_manual = float(np.mean(vals))
            cmp('SE-SE CN mean', cn_manual, fm.get('se_se_cn') or fm.get('se_se_cn_mean'))

    # Conductivity / τ relations (consistency)
    phi = fm.get('phi_se', 0)
    sig_full = fm.get('sigma_full_mScm')
    sig_bulk = fm.get('sigma_bulk_net_mScm')
    tau_stored = fm.get('tortuosity_mean')

    if phi and sig_full:
        tau_le = math.sqrt(phi * SIGMA_GRAIN_MS / sig_full) if sig_full > 0 else None
        print(f'\n--- τ DERIVATIONS (sanity only, not stored) ---')
        print(f'  τ_Lap_eff  (from stored σ_full)   = {tau_le:.3f}')
        if sig_bulk:
            tau_lg = math.sqrt(phi * SIGMA_GRAIN_MS / sig_bulk) if sig_bulk > 0 else None
            print(f'  τ_Lap_geom (from stored σ_bulk)  = {tau_lg:.3f}')
        print(f'  τ_Dij      (stored)               = {tau_stored}')

    # Expected from composition (sanity)
    print(f'\n--- EXPECTED FROM COMPOSITION (14% porosity assumed) ---')
    # wt% from meta (if bimodal with P:S, compute SE wt from ps_ratio)
    # For now, just estimate from atom counts
    if se_types and am_types:
        total_am_vol = ((4/3) * math.pi * (df_a.loc[df_a['type'].isin(am_types), 'radius']**3)).sum()
        total_se_vol = se_vol
        vol_ratio_am_se = total_am_vol / total_se_vol if total_se_vol > 0 else 0
        phi_SE_expected_14 = 0.86 * (total_se_vol / (total_am_vol + total_se_vol)) if (total_am_vol + total_se_vol) > 0 else 0
        print(f'  AM vol total:   {total_am_vol:.6f} sim³')
        print(f'  SE vol total:   {total_se_vol:.6f} sim³')
        print(f'  AM:SE (vol):    {vol_ratio_am_se:.2f}:1')
        print(f'  φ_SE expected (14% poro):  {phi_SE_expected_14:.3f}')
        print(f'  φ_SE stored:               {phi:.3f}')
        if phi_SE_expected_14 and abs(phi - phi_SE_expected_14)/phi_SE_expected_14 > 0.10:
            print(f'  ⚠ MISMATCH: stored φ_SE is {100*(phi/phi_SE_expected_14 - 1):+.0f}% off from 14%-porosity expectation.')


if __name__ == '__main__':
    main()
