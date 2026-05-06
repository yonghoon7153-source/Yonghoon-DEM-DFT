#!/usr/bin/env python3
"""Audit UI layout consistency across all cases.

Simulates the webapp's network_summary table construction pipeline for
every discoverable case (webapp/results/* + webapp/archive/**) and
reports any cases whose final layout differs from the canonical structure.

Usage:
    python3 scripts/audit_ui_layout.py
    python3 scripts/audit_ui_layout.py --verbose
    python3 scripts/audit_ui_layout.py --case input_1mAh_100_10

Output groups cases by 'layout fingerprint' (ordered list of section
headers + label-only row sequence). All cases SHOULD share one
fingerprint after our normalize pass. Any deviation indicates a missed
layout variant that needs patching in normalize_network_summary_layout().
"""
from __future__ import annotations
import argparse
import json
import os
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WEBAPP = ROOT / 'webapp'
sys.path.insert(0, str(WEBAPP))

# Inject minimal config so app.py imports succeed
os.environ.setdefault('FLASK_ENV', 'production')

import app as webapp  # noqa: E402


def _find_cases():
    out = []
    rroot = WEBAPP / 'results'
    aroot = WEBAPP / 'archive'
    uploads = WEBAPP / 'uploads'

    if rroot.is_dir():
        for d in sorted(rroot.iterdir()):
            if not d.is_dir() or d.name in ('reports', 'group_plots'):
                continue
            ns = d / 'network_summary.csv'
            fm = d / 'full_metrics.json'
            meta_p = uploads / d.name / 'meta.json'
            if ns.exists() and fm.exists() and meta_p.exists():
                out.append((d.name, d, meta_p, 'results'))
    if aroot.is_dir():
        for meta_p in sorted(aroot.rglob('meta.json')):
            d = meta_p.parent
            if (d / 'network_summary.csv').exists() and (d / 'full_metrics.json').exists():
                out.append((d.name, d, meta_p, 'archive'))
    return out


def _build_table(case_dir: Path, meta_path: Path):
    """Mirror webapp's table-construction pipeline for one case."""
    import csv

    with open(meta_path) as f:
        meta = json.load(f)
    fm_path = case_dir / 'full_metrics.json'
    with open(fm_path) as f:
        metrics = json.load(f)
    ns_path = case_dir / 'network_summary.csv'
    rows = []
    with open(ns_path) as f:
        rdr = csv.reader(f)
        cols = next(rdr)
        for r in rdr:
            rows.append(r)
    # Pad each row to len(cols)
    while len(cols) < 4:
        cols.append('')
    cols = ['지표', 'Hertzian (DEM-native)', 'Physics (Tabor+volume)', 'Δ (%)']
    expanded = []
    for r in rows:
        row = list(r) + [''] * (4 - len(r))
        expanded.append(row[:4])

    tables = {'network_summary': {'columns': cols, 'data': expanded}}

    # Load input_params
    input_params = {}
    pp = case_dir / 'input_params.json'
    if pp.exists():
        with open(pp) as f:
            input_params = json.load(f)
    if 'scale' not in input_params:
        input_params['scale'] = meta.get('scale', 1)

    # Run the actual webapp pipeline
    webapp.transform_network_summary_4col(tables, metrics, meta)
    webapp.inject_tier1_patch_rows(tables, metrics)
    webapp.inject_stage_e_rows(tables, metrics)
    webapp.inject_cell_asr_rows(tables, metrics, input_params)
    webapp.normalize_network_summary_layout(tables, metrics)
    webapp.apply_paper_labels(tables)

    return tables['network_summary']


def _layout_fingerprint(table):
    """Layout signature: ordered tuple of (kind, label) where kind is
    'section' for headers and 'row' for data rows. Only the LABEL is
    used (col 0), values are ignored."""
    sig = []
    for r in table['data']:
        if not r or not r[0]:
            continue
        lbl = r[0].strip() if isinstance(r[0], str) else ''
        if lbl.startswith('──'):
            sig.append(('section', lbl))
        else:
            sig.append(('row', lbl))
    return tuple(sig)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--verbose', '-v', action='store_true',
                    help='Print full layout for each variant')
    ap.add_argument('--case', help='Print layout for one case only')
    args = ap.parse_args()

    cases = _find_cases()
    print(f'Discovered {len(cases)} cases')

    if args.case:
        match = [c for c in cases if c[0] == args.case]
        if not match:
            print(f'  no case named {args.case!r}')
            return
        cid, d, meta, src = match[0]
        try:
            tbl = _build_table(d, meta)
        except Exception as e:
            print(f'  ERROR: {type(e).__name__}: {e}')
            return
        for r in tbl['data']:
            print('  ', r)
        return

    fingerprints = defaultdict(list)
    errors = []
    for cid, d, meta, src in cases:
        try:
            tbl = _build_table(d, meta)
            fp = _layout_fingerprint(tbl)
            fingerprints[fp].append((cid, src))
        except Exception as e:
            errors.append((cid, f'{type(e).__name__}: {e}'))

    print(f'\nLayout fingerprints: {len(fingerprints)} distinct variant(s)')
    if errors:
        print(f'  ✗ {len(errors)} cases failed:')
        for cid, e in errors[:5]:
            print(f'    {cid}: {e}')

    sorted_fps = sorted(fingerprints.items(), key=lambda x: -len(x[1]))
    for i, (fp, members) in enumerate(sorted_fps, 1):
        print(f'\n=== Variant {i}: {len(members)} case(s) ===')
        examples = ', '.join(c for c, _ in members[:5])
        if len(members) > 5:
            examples += f', ... (+{len(members)-5})'
        print(f'  examples: {examples}')

        # Compute diff vs Variant 1 (most common)
        if i == 1:
            print(f'  [reference layout — {len(fp)} rows]')
            if args.verbose:
                for kind, lbl in fp:
                    prefix = '──' if kind == 'section' else '  '
                    print(f'    {prefix} {lbl}')
        else:
            ref_fp = sorted_fps[0][0]
            ref_set = {(k, l) for k, l in ref_fp}
            this_set = {(k, l) for k, l in fp}
            missing = ref_set - this_set
            extra = this_set - ref_set
            if missing:
                print(f'  MISSING vs reference ({len(missing)}):')
                for kind, lbl in sorted(missing):
                    print(f'    - {kind}: {lbl}')
            if extra:
                print(f'  EXTRA vs reference ({len(extra)}):')
                for kind, lbl in sorted(extra):
                    print(f'    + {kind}: {lbl}')
            if not missing and not extra:
                print(f'  (same set of rows but in different order)')


if __name__ == '__main__':
    main()
