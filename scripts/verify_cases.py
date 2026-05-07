#!/usr/bin/env python3
"""Verify all expected pipeline triggers ran for every case.

Audits each case's full_metrics.json for the presence of fields written
by each pipeline stage. Reports incomplete cases so they can be re-run
manually:
    bash scripts/run baseline <case>     # if Network Solver missing
    bash scripts/run stagee   <case>     # if Stage E missing

Usage:
    python3 scripts/verify_cases.py            # report all incomplete
    python3 scripts/verify_cases.py --fix      # auto-run missing stages
    python3 scripts/verify_cases.py CASE_ID    # one case
"""
from __future__ import annotations
import argparse
import json
import subprocess
import sys
from pathlib import Path


# Pipeline stages and the metrics keys each one writes (presence = stage ran)
STAGES = [
    ('contact_analysis', [
        'porosity', 'thickness_um', 'percolation_pct',
        'sigma_full_mScm',  # written by analyze_contacts.py via network merge
    ]),
    ('coverage_physics', [
        'coverage_AM_mean_physics_rough',  # B3 shape-corrected coverage
        'area_AM전체_SE_total_physics',    # Tabor-area total
    ]),
    ('network_solver_baseline', [
        'electronic_sigma_full_mScm',
        'thermal_sigma_full_mScm',
        'sigma_full_mScm_physics',
    ]),
    ('stage_e', [
        'sigma_full_mScm_stage_e',
        'electronic_sigma_full_mScm_stage_e',
        'thermal_sigma_full_mScm_stage_e',
        'stage_e_factors_used',
        'stage_e_source',
    ]),
    ('tier1_patches', [
        'coverage_AM_mean_physics_rough',  # B3
        'se_se_cn_perc',                   # F2
        'se_se_cn_eff_area',               # F2
        'se_se_cn_aug',                    # F1
    ]),
]

REPAIR_CMDS = {
    'contact_analysis':         'bash scripts/run baseline {cid}',
    'coverage_physics':         'bash scripts/run baseline {cid}',
    'network_solver_baseline':  'bash scripts/run baseline {cid}',
    'stage_e':                  'bash scripts/run stagee {cid}',
    'tier1_patches':            'bash scripts/run baseline {cid}',
}


def _check_one(case_dir: Path) -> dict:
    fm_path = case_dir / 'full_metrics.json'
    if not fm_path.exists():
        return {'ok': False, 'missing_file': True, 'missing_stages': []}
    with open(fm_path) as f:
        m = json.load(f)
    if m.get('mode_note', '').startswith('atoms_only'):
        return {'ok': True, 'atoms_only': True, 'missing_stages': []}

    missing = []
    for stage, keys in STAGES:
        if any(m.get(k) is None for k in keys):
            absent_keys = [k for k in keys if m.get(k) is None]
            missing.append((stage, absent_keys))
    return {'ok': not missing, 'missing_stages': missing}


def main():
    ap = argparse.ArgumentParser(description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('case_id', nargs='?')
    ap.add_argument('--fix', action='store_true',
                    help='Auto-run missing stages (slow)')
    args = ap.parse_args()

    root = Path('webapp')
    cases = []
    for fm in root.rglob('full_metrics.json'):
        case_dir = fm.parent
        if args.case_id and case_dir.name != args.case_id:
            continue
        cases.append(case_dir)

    if not cases:
        print('No cases found.')
        return

    print(f'Verifying {len(cases)} cases...\n')

    incomplete = []
    atoms_only = 0
    for case_dir in sorted(cases):
        r = _check_one(case_dir)
        if r.get('atoms_only'):
            atoms_only += 1
            continue
        if not r['ok']:
            incomplete.append((case_dir.name, r['missing_stages']))

    print(f'Summary: {len(cases) - len(incomplete) - atoms_only} complete,'
          f' {len(incomplete)} incomplete, {atoms_only} atoms-only.\n')

    if not incomplete:
        print('✓ All cases have complete pipeline output.')
        return

    print(f'✗ {len(incomplete)} case(s) missing pipeline stages:')
    repairs = []
    for cid, miss in incomplete:
        print(f'\n  {cid}')
        for stage, keys in miss:
            print(f'    - {stage}  (missing keys: {", ".join(keys[:3])}'
                  f"{', ...' if len(keys) > 3 else ''})")
            repairs.append((cid, stage))

    if args.fix:
        print(f'\n=== Auto-fixing {len(repairs)} (cid, stage) pairs ===')
        # Dedup: each case may need multiple commands; collapse to unique cmds
        unique_cmds = sorted({REPAIR_CMDS[s].format(cid=c) for c, s in repairs})
        for cmd in unique_cmds:
            print(f'  $ {cmd}')
            subprocess.run(cmd, shell=True)
    else:
        print('\nRun with --fix to auto-repair, or manually:')
        seen_cmds = set()
        for c, s in repairs:
            cmd = REPAIR_CMDS[s].format(cid=c)
            if cmd not in seen_cmds:
                seen_cmds.add(cmd)
                print(f'  {cmd}')


if __name__ == '__main__':
    main()
