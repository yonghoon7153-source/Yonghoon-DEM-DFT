#!/usr/bin/env python3
"""B2 + B4 diagnostic — AM-AM area dominance + AM-AM overlap variation.

Two diagnostics to settle whether B2 (AM-AM area subtraction) and B4
(AM deformation) are model-noise-level or critical:

  B2 diagnostic: For each case, compute per-AM
    • AM-AM contact area total
    • AM total surface = 4π R²
    • Ratio = AM-AM contact / total surface
  Aggregate across all 76+ cases. If most AMs show <5% AM-AM area,
  B2 is noise-level. If 10%+ AMs have >20% AM-AM area, B2 is critical.

  B4 diagnostic: For each AM-AM contact in the dataset
    • Hertzian overlap δ
    • Hertzian overlap ratio δ/R_min
  Distribution across cases. If max(δ/R) < 0.005, AM essentially rigid
  (plastic regime starts at ~0.0011 per Tabor). If significant fraction
  exceeds 0.005, AM deforming → B4 matters.
"""
from __future__ import annotations
import sys, json, warnings
from pathlib import Path
import numpy as np
import pandas as pd
from collections import defaultdict

SCRIPTS = Path(__file__).parent
sys.path.insert(0, str(SCRIPTS))
warnings.filterwarnings('ignore')

WEBAPP = SCRIPTS.parent / 'webapp'


def parse_type_map(s):
    out = {}
    for tok in s.split(','):
        if ':' in tok:
            k, v = tok.split(':', 1)
            try: out[int(k.strip())] = v.strip()
            except: pass
    return out


def find_case_dir(cid):
    for base in ('webapp/results', 'webapp/archive'):
        for p in Path(base).rglob(f'{cid}'):
            if p.is_dir() and (p / 'atoms.csv').exists():
                return p
    return None


def diagnose_one_case(case_dir, type_map):
    """Return dict with per-AM stats for B2 + B4."""
    atoms_df = pd.read_csv(case_dir / 'atoms.csv')
    contacts_df = pd.read_csv(case_dir / 'contacts.csv', low_memory=False)

    # AM types in this case
    am_types = {tid for tid, lbl in type_map.items() if 'AM' in lbl}
    se_types = {tid for tid, lbl in type_map.items() if lbl == 'SE'}

    # Per-AM info
    am_info = {}
    for _, row in atoms_df.iterrows():
        if int(row['type']) in am_types:
            r = float(row['radius'])
            am_info[int(row['id'])] = {
                'radius': r,
                'surface': 4 * np.pi * r ** 2,  # μm² (in DEM scale, but ratio is dimensionless)
                'am_am_area': 0.0,
                'am_se_area': 0.0,
                'am_am_overlap_max': 0.0,
                'am_am_overlap_count': 0,
                'type': type_map[int(row['type'])],
            }

    # Iterate contacts
    am_am_overlaps = []
    for _, c in contacts_df.iterrows():
        i1, i2 = int(c['id1']), int(c['id2'])
        if i1 not in am_info and i2 not in am_info: continue
        atype1 = atoms_df[atoms_df['id'] == i1].iloc[0] if (atoms_df['id'] == i1).any() else None
        atype2 = atoms_df[atoms_df['id'] == i2].iloc[0] if (atoms_df['id'] == i2).any() else None
        if atype1 is None or atype2 is None: continue
        t1, t2 = int(atype1['type']), int(atype2['type'])
        area = float(c.get('contact_area', 0) or 0)
        delta = float(c.get('delta', 0) or 0)

        if t1 in am_types and t2 in am_types:
            # AM-AM contact
            r1 = am_info[i1]['radius']; r2 = am_info[i2]['radius']
            r_min = min(r1, r2)
            am_info[i1]['am_am_area'] += area
            am_info[i2]['am_am_area'] += area
            if delta > 0 and r_min > 0:
                ratio = delta / r_min
                am_am_overlaps.append(ratio)
                am_info[i1]['am_am_overlap_count'] += 1
                am_info[i2]['am_am_overlap_count'] += 1
                am_info[i1]['am_am_overlap_max'] = max(
                    am_info[i1]['am_am_overlap_max'], ratio)
                am_info[i2]['am_am_overlap_max'] = max(
                    am_info[i2]['am_am_overlap_max'], ratio)
        elif (t1 in am_types and t2 in se_types) or \
             (t2 in am_types and t1 in se_types):
            am_id = i1 if t1 in am_types else i2
            am_info[am_id]['am_se_area'] += area

    # Per-AM ratios
    ratios_AMP = []; ratios_AMS = []
    for aid, info in am_info.items():
        if info['surface'] <= 0: continue
        r = info['am_am_area'] / info['surface']
        if info['type'] == 'AM_P':
            ratios_AMP.append(r)
        elif info['type'] == 'AM_S':
            ratios_AMS.append(r)
    return {
        'n_AMP': len(ratios_AMP),
        'n_AMS': len(ratios_AMS),
        'AMP_amam_ratio_mean': float(np.mean(ratios_AMP)) if ratios_AMP else None,
        'AMP_amam_ratio_median': float(np.median(ratios_AMP)) if ratios_AMP else None,
        'AMP_amam_ratio_max': float(np.max(ratios_AMP)) if ratios_AMP else None,
        'AMS_amam_ratio_mean': float(np.mean(ratios_AMS)) if ratios_AMS else None,
        'AMS_amam_ratio_median': float(np.median(ratios_AMS)) if ratios_AMS else None,
        'AMS_amam_ratio_max': float(np.max(ratios_AMS)) if ratios_AMS else None,
        'am_am_overlap_n': len(am_am_overlaps),
        'am_am_overlap_max': float(np.max(am_am_overlaps)) if am_am_overlaps else 0.0,
        'am_am_overlap_median': float(np.median(am_am_overlaps)) if am_am_overlaps else 0.0,
        'am_am_overlap_p95': float(np.percentile(am_am_overlaps, 95))
                              if am_am_overlaps else 0.0,
    }


def main():
    paths = list(Path('webapp/results').glob('*/full_metrics.json')) + \
            list(Path('webapp/archive').rglob('*/full_metrics.json'))
    case_ids = list({p.parent.name for p in paths})
    print(f'Diagnosing B2+B4 across {len(case_ids)} cases...', flush=True)

    all_results = []
    n_processed = 0
    for cid in case_ids:
        case_dir = find_case_dir(cid)
        if case_dir is None: continue
        # type_map
        meta_p = case_dir / 'meta.json'
        if not meta_p.exists():
            up = WEBAPP / 'uploads' / cid / 'meta.json'
            meta_p = up if up.exists() else None
        type_map = {1: 'AM_P', 2: 'AM_S', 3: 'SE'}
        if meta_p:
            try:
                m = json.load(open(meta_p))
                tm = parse_type_map(m.get('type_map', ''))
                if tm: type_map = tm
            except Exception: pass
        try:
            r = diagnose_one_case(case_dir, type_map)
            r['case_id'] = cid
            all_results.append(r)
            n_processed += 1
        except Exception as e:
            print(f'  {cid}: {e}', flush=True)
        if n_processed % 20 == 0 and n_processed > 0:
            print(f'  {n_processed}/{len(case_ids)} processed', flush=True)

    print(f'\n  successfully diagnosed: {len(all_results)} cases', flush=True)

    df = pd.DataFrame(all_results)

    # ── B2 summary ────────────────────────────────────────────
    print('\n' + '=' * 80, flush=True)
    print('B2 DIAGNOSTIC — AM-AM area / AM total surface ratio', flush=True)
    print('=' * 80, flush=True)
    print('\nAcross all cases, mean AM-AM area / total surface ratio:', flush=True)
    for col, label in [('AMP_amam_ratio_mean', 'AM_P (polycryst, large)'),
                        ('AMS_amam_ratio_mean', 'AM_S (single cryst, small)')]:
        v = df[col].dropna().values
        if len(v) == 0: continue
        print(f'  {label:30s}  median = {np.median(v):.3f}  '
              f'mean = {v.mean():.3f}  max = {v.max():.3f}', flush=True)

    print('\n  Verdict — B2 dominance:', flush=True)
    amp_mean = df['AMP_amam_ratio_mean'].dropna().mean()
    ams_mean = df['AMS_amam_ratio_mean'].dropna().mean()
    print(f'    AM_P mean ratio: {amp_mean:.3f}', flush=True)
    print(f'    AM_S mean ratio: {ams_mean:.3f}', flush=True)
    if amp_mean > 0.20 or ams_mean > 0.20:
        print('    🔴 AM-AM contact area > 20% of surface — B2 critical, '
              'need refined model.', flush=True)
    elif amp_mean > 0.10 or ams_mean > 0.10:
        print('    🟡 AM-AM area significant (10-20%) — B2 worth refining.',
              flush=True)
    else:
        print('    🟢 AM-AM area < 10% — B2 is noise-level, current '
              'subtraction acceptable.', flush=True)

    # ── B4 summary ────────────────────────────────────────────
    print('\n' + '=' * 80, flush=True)
    print('B4 DIAGNOSTIC — AM-AM overlap (δ/R) variation', flush=True)
    print('=' * 80, flush=True)
    print('\nAM-AM Hertzian overlap distribution (δ/R_min):', flush=True)
    print(f'  Plastic regime starts at ~0.0011 (Tabor yield)', flush=True)
    print(f'  Fully plastic: ~0.0078\n', flush=True)
    overlaps = df['am_am_overlap_median'].dropna().values
    overlaps_max = df['am_am_overlap_max'].dropna().values
    overlaps_p95 = df['am_am_overlap_p95'].dropna().values
    if len(overlaps) > 0:
        print(f'  per-case median overlap:  '
              f'{np.median(overlaps):.4f} (median across cases)', flush=True)
        print(f'  per-case max overlap:     '
              f'{np.median(overlaps_max):.4f} (median across cases)',
              flush=True)
        print(f'  per-case 95th-percentile: '
              f'{np.median(overlaps_p95):.4f} (median across cases)',
              flush=True)
        print(f'  GLOBAL maximum across all cases: '
              f'{overlaps_max.max():.4f}', flush=True)

        n_yielded = (df['am_am_overlap_max'] > 0.0011).sum()
        n_plastic = (df['am_am_overlap_max'] > 0.0078).sum()
        print(f'\n  Cases with at least one AM-AM contact in:', flush=True)
        print(f'    elastic-plastic transition (δ/R > 0.0011): '
              f'{n_yielded}/{len(df)}', flush=True)
        print(f'    fully plastic regime       (δ/R > 0.0078): '
              f'{n_plastic}/{len(df)}', flush=True)
        print(f'\n  Verdict — B4 (AM deformation):', flush=True)
        if n_plastic > len(df) * 0.3:
            print('    🔴 AM significantly deforming in many cases — '
                  'B4 critical, soft AM assumption wrong.', flush=True)
        elif n_yielded > len(df) * 0.5:
            print('    🟡 AM at yield onset frequently — B4 mild '
                  'consideration.', flush=True)
        else:
            print('    🟢 AM mostly elastic — B4 minor, current rigid-AM '
                  'assumption acceptable.', flush=True)

    # Save full results
    out = Path('docs/figures/physics_regime')
    out.mkdir(parents=True, exist_ok=True)
    df.to_csv(out / 'b2_b4_diagnostic.csv', index=False)
    print(f'\n→ {out}/b2_b4_diagnostic.csv', flush=True)


if __name__ == '__main__':
    main()
