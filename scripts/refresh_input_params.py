#!/usr/bin/env python3
"""
Regenerate input_params.json for every case by re-parsing the uploaded
input_*.liggghts with the current (robust) parser.

Does NOT touch atoms.csv / contacts.csv / network_conductivity.json —
only the input_params.json file is rewritten. Safe to run anytime after a
parser upgrade (e.g. commit b88fd39 which added ${var}/arithmetic support).

Usage:
  python3 scripts/refresh_input_params.py                    # all cases
  python3 scripts/refresh_input_params.py 260421_212503_cb59a9 ...  # selected
"""
from __future__ import annotations
import os, sys, json, glob

sys.path.insert(0, os.path.dirname(__file__))
from parse_liggghts import parse_input_script


UPLOADS = 'webapp/uploads'
RESULTS = 'webapp/results'


def refresh_one(case_id: str) -> tuple[str, dict]:
    upload_dir = os.path.join(UPLOADS, case_id)
    results_dir = os.path.join(RESULTS, case_id)

    if not os.path.isdir(upload_dir):
        return 'no_upload_dir', {}

    # Find the input_*.liggghts
    candidates = sorted(glob.glob(os.path.join(upload_dir, 'input*.liggghts')))
    if not candidates:
        return 'no_input_script', {}

    # Pick the last one alphabetically (usually a single file per case)
    params = parse_input_script(candidates[-1])

    if not params or 'box_x' not in params:
        return 'parse_failed_or_missing_box', params

    # Write to results_dir (that's where app.py reads from)
    if not os.path.isdir(results_dir):
        os.makedirs(results_dir, exist_ok=True)
    target = os.path.join(results_dir, 'input_params.json')
    with open(target, 'w') as f:
        json.dump(params, f, indent=2)

    return 'ok', params


def main():
    if not os.path.isdir(UPLOADS):
        print(f'ERROR: {UPLOADS} not found (run from project root)')
        sys.exit(1)

    if len(sys.argv) > 1:
        case_ids = sys.argv[1:]
    else:
        case_ids = sorted(os.listdir(UPLOADS))

    stats = {'ok': 0, 'no_input_script': 0, 'no_upload_dir': 0,
             'parse_failed_or_missing_box': 0}

    print(f'Refreshing input_params.json for {len(case_ids)} case(s)...\n')
    for cid in case_ids:
        status, params = refresh_one(cid)
        stats[status] = stats.get(status, 0) + 1
        box_info = ''
        if status == 'ok':
            bx = params.get('box_x', 0)
            by = params.get('box_y', 0)
            box_info = f'box={bx}×{by} (sim)'
        print(f'  [{status:30s}] {cid}  {box_info}')

    print()
    print('Summary:')
    for k, v in stats.items():
        print(f'  {k:32s} {v}')


if __name__ == '__main__':
    main()
