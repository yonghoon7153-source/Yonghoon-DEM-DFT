#!/usr/bin/env python3
"""Walk archive directories and produce a flat CSV of every DEM case's
composition + measured porosity.

Schema discovered from webapp/archive/*/*/full_metrics.json:
    porosity         (percent, top-level)
    am_se_ratio      "AA:BB"   (top-level)
    ps_ratio         "P:S"     (in meta.json, may be empty for monomodal)
    n_AM_P, r_AM_P   (optional — trimodal cases)
    n_AM_S, r_AM_S
    n_SE,   r_SE
    scale            (in meta.json, e.g. 1000)

Output columns:
    case_id, campaign, am_wt, se_wt, p_vol, s_vol,
    n_AM_P, r_AM_P_um, n_AM_S, r_AM_S_um, n_SE, r_SE_um,
    scale, porosity_pct

Usage:
    python3 scripts/collect_porosity_cases.py <root1> [<root2> ...]
"""
import json
import sys
import csv
from pathlib import Path


def parse_ratio(s):
    if not s or ':' not in str(s):
        return None, None
    try:
        a, b = str(s).split(':')[:2]
        return float(a), float(b)
    except Exception:
        return None, None


def safe_load(p: Path):
    try:
        return json.loads(p.read_text())
    except Exception:
        return None


def collect(root: Path, rows: list):
    if not root.exists():
        print(f'  skip: {root} (not found)')
        return
    n = 0
    for fm_path in sorted(root.rglob('full_metrics.json')):
        case_dir = fm_path.parent
        fm = safe_load(fm_path)
        if not fm:
            continue
        meta = safe_load(case_dir / 'meta.json') or {}
        ip   = safe_load(case_dir / 'input_params.json') or {}

        poro = fm.get('porosity')
        if poro is None:
            continue

        # composition
        am_wt, se_wt = parse_ratio(
            fm.get('am_se_ratio') or ip.get('am_se_ratio'))
        ps = fm.get('ps_ratio') or meta.get('ps_ratio')
        p_vol, s_vol = parse_ratio(ps)

        # scale & particle sizes — r_* in full_metrics is sim units (m);
        # multiply by 1e6 to get µm of the SIMULATION box, then divide
        # by scale to recover physical µm.  Pure sim values are kept
        # if scale missing.
        scale = meta.get('scale') or ip.get('scale') or 1.0
        def r_phys(key):
            r = fm.get(key)
            if r is None:
                return None
            return r * 1e6 / float(scale)  # m → µm physical

        rows.append({
            'case_id':   case_dir.name,
            'campaign':  root.name,
            'am_wt':     am_wt,
            'se_wt':     se_wt,
            'p_vol':     p_vol,
            's_vol':     s_vol,
            'n_AM_P':    fm.get('n_AM_P'),
            'r_AM_P_um': r_phys('r_AM_P'),
            'n_AM_S':    fm.get('n_AM_S'),
            'r_AM_S_um': r_phys('r_AM_S'),
            'n_SE':      fm.get('n_SE'),
            'r_SE_um':   r_phys('r_SE'),
            'scale':     scale,
            'porosity_pct': round(float(poro), 3),
        })
        n += 1
    print(f'  {root}: {n} cases')


def main():
    if len(sys.argv) < 2:
        print('usage: collect_porosity_cases.py <root1> [<root2> ...]')
        sys.exit(1)
    rows = []
    for arg in sys.argv[1:]:
        collect(Path(arg), rows)
    rows.sort(key=lambda r: (r['campaign'], r['case_id']))
    out = Path('all_dem_porosity.csv')
    fieldnames = ['case_id', 'campaign', 'am_wt', 'se_wt', 'p_vol', 's_vol',
                  'n_AM_P', 'r_AM_P_um', 'n_AM_S', 'r_AM_S_um',
                  'n_SE', 'r_SE_um', 'scale', 'porosity_pct']
    with out.open('w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)
    print(f'\nWrote {len(rows)} cases → {out.resolve()}')


if __name__ == '__main__':
    main()
