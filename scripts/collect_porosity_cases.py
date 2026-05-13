#!/usr/bin/env python3
"""Walk webapp/uploads/ (and any extra dir given on CLI) and produce a
flat CSV of every DEM case's composition + measured porosity.

Output columns:
    case_id, am_wt, se_wt, p_vol, s_vol, r_se_um, scale, porosity_pct

Usage:
    python3 scripts/collect_porosity_cases.py                # webapp/uploads
    python3 scripts/collect_porosity_cases.py path1 path2    # extra roots
"""
import json
import sys
import csv
from pathlib import Path


def parse_ratio(s):
    if not s or ':' not in str(s):
        return None, None
    a, b = str(s).split(':')[:2]
    try:
        return float(a), float(b)
    except ValueError:
        return None, None


def collect(root: Path, rows: list):
    if not root.exists():
        return
    for meta in root.rglob('meta.json'):
        case_dir = meta.parent
        ip = case_dir / 'input_params.json'
        fm = case_dir / 'full_metrics.json'
        try:
            m = json.loads(meta.read_text())
        except Exception:
            continue
        ip_data = {}
        if ip.exists():
            try:
                ip_data = json.loads(ip.read_text())
            except Exception:
                pass
        # porosity may be in meta.json or full_metrics.json
        poro = m.get('porosity')
        if poro is None and fm.exists():
            try:
                fmd = json.loads(fm.read_text())
                poro = fmd.get('porosity', {}).get('value')
            except Exception:
                pass
        if poro is None:
            continue

        am_wt, se_wt = parse_ratio(ip_data.get('am_se_ratio'))
        p_vol, s_vol = parse_ratio(ip_data.get('p_s_ratio'))
        r_se = (ip_data.get('r_SE_um')
                or ip_data.get('r_se')
                or ip_data.get('SE_radius_um'))
        scale = ip_data.get('scale') or ip_data.get('Scale')

        rows.append({
            'case_id':  case_dir.name,
            'am_wt':    am_wt,
            'se_wt':    se_wt,
            'p_vol':    p_vol,
            's_vol':    s_vol,
            'r_se_um':  r_se,
            'scale':    scale,
            'porosity_pct': poro,
        })


def main():
    roots = [Path('webapp/uploads')]
    roots.extend(Path(p) for p in sys.argv[1:])
    rows = []
    for r in roots:
        collect(r, rows)
    rows.sort(key=lambda x: x['case_id'])
    out = Path('all_dem_porosity.csv')
    fieldnames = ['case_id', 'am_wt', 'se_wt', 'p_vol', 's_vol',
                  'r_se_um', 'scale', 'porosity_pct']
    with out.open('w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)
    print(f'Wrote {len(rows)} cases → {out.resolve()}')
    if rows:
        print('\nfirst few rows:')
        for r in rows[:5]:
            print(' ', r)


if __name__ == '__main__':
    main()
