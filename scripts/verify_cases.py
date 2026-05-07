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


# Pipeline stages and the metrics keys each one writes (presence = stage ran).
#
# Two severity tiers:
#   CRITICAL — UI cannot render correctly without these (require repair).
#   COSMETIC — older cases predate the field; UI shows '—' placeholder.
#              Repair is OPTIONAL (only matters for newly added analyses).
STAGES_CRITICAL = [
    ('contact_analysis', [
        'porosity', 'thickness_um', 'percolation_pct',
        'sigma_full_mScm',  # baseline σ_ionic — required for ASR + Stage E delta
    ]),
    ('stage_e_values', [
        'sigma_full_mScm_stage_e',          # Stage E σ_ionic value
        # Note: σ_e/κ Stage E intentionally NOT critical — they're None when
        # the channel has no AM-AM (P:S=0:10) or no κ baseline.
    ]),
]

STAGES_COSMETIC = [
    ('coverage_physics_rough', [
        'coverage_AM_mean_physics_rough',  # B3 shape-corrected (added later)
    ]),
    ('stage_e_source_meta', [
        'stage_e_source',  # Bruggeman fallback metadata (added in commit 7a11682)
    ]),
    ('tier1_patches', [
        'se_se_cn_perc', 'se_se_cn_eff_area',
        'se_se_cn_eff_area_perc', 'se_se_cn_aug',
    ]),
]

REPAIR_CMDS = {
    'contact_analysis':       'bash scripts/run baseline {cid}',
    'stage_e_values':         'bash scripts/run stagee {cid}',
    'coverage_physics_rough': 'bash scripts/run baseline {cid}',
    'stage_e_source_meta':    'bash scripts/run stagee {cid}',
    'tier1_patches':          'bash scripts/run baseline {cid}',
}


def _check_one(case_dir: Path) -> dict:
    fm_path = case_dir / 'full_metrics.json'
    if not fm_path.exists():
        return {'ok': False, 'missing_file': True,
                'critical': [], 'cosmetic': []}
    with open(fm_path) as f:
        m = json.load(f)
    if m.get('mode_note', '').startswith('atoms_only'):
        return {'ok': True, 'atoms_only': True,
                'critical': [], 'cosmetic': []}

    critical = []
    for stage, keys in STAGES_CRITICAL:
        absent = [k for k in keys if m.get(k) is None]
        if absent:
            critical.append((stage, absent))

    cosmetic = []
    for stage, keys in STAGES_COSMETIC:
        absent = [k for k in keys if m.get(k) is None]
        if absent:
            cosmetic.append((stage, absent))

    return {'ok': not critical, 'critical': critical, 'cosmetic': cosmetic}


def main():
    ap = argparse.ArgumentParser(description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('case_id', nargs='?')
    ap.add_argument('--fix', action='store_true',
                    help='Auto-run missing CRITICAL stages')
    ap.add_argument('--include-cosmetic', action='store_true',
                    help='Also report (and --fix) cosmetic missing fields')
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

    print(f'Verifying {len(cases)} cases (cosmetic={"on" if args.include_cosmetic else "off"})...\n')

    critical_cases = []
    cosmetic_cases = []
    atoms_only = 0
    for case_dir in sorted(cases):
        r = _check_one(case_dir)
        if r.get('atoms_only'):
            atoms_only += 1
            continue
        if r['critical']:
            critical_cases.append((case_dir.name, r['critical']))
        elif r['cosmetic'] and args.include_cosmetic:
            cosmetic_cases.append((case_dir.name, r['cosmetic']))

    n_complete = len(cases) - len(critical_cases) - atoms_only
    print(f'Summary: {n_complete}/{len(cases)} complete (UI render-ready),'
          f' {len(critical_cases)} CRITICAL,'
          f' {atoms_only} atoms-only.\n')

    if not critical_cases:
        print('✓ All cases UI-render-ready (no critical missing fields).')
        if cosmetic_cases:
            print(f'\n  ({len(cosmetic_cases)} cases have cosmetic gaps —'
                  f' older code metadata, UI shows — placeholder. Use'
                  f' --include-cosmetic to list them.)')
        return

    print(f'✗ {len(critical_cases)} case(s) with CRITICAL missing data:')
    repairs = []
    for cid, miss in critical_cases:
        print(f'\n  {cid}')
        for stage, keys in miss:
            print(f'    - {stage}  (missing: {", ".join(keys[:3])}'
                  f"{', ...' if len(keys) > 3 else ''})")
            repairs.append((cid, stage))

    if args.include_cosmetic and cosmetic_cases:
        print(f'\n--- Cosmetic gaps ({len(cosmetic_cases)} cases) ---')
        for cid, miss in cosmetic_cases:
            print(f'  {cid}: {", ".join(s for s, _ in miss)}')

    if args.fix:
        print(f'\n=== Auto-fixing {len(repairs)} CRITICAL (cid, stage) pairs ===')
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
