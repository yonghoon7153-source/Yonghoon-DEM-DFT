#!/usr/bin/env python3
"""Audit every case for missing Stage E / ASR / validation_flags fields
and classify cases by what's wrong + suggest a single fix command.

Walks webapp/archive/** and webapp/results/** for every full_metrics.json,
inspects which fields are populated, and prints a per-case report card.
Categorises every case into one of:

  ✓ complete            — Stage E σ_ionic, σ_e, κ + ASR + validation_flags
  ~ partial-stage-e     — some Stage E channels missing
  ⚠ no-stage-e          — Stage E never ran (only baseline metrics)
  ⚠ no-validation-flags — Stage E ran but no validation_flags self-report
  ✗ no-baseline         — full_metrics.json malformed / pipeline never ran

At the end, prints a one-shot fix command (find_and_rerun_stage_e.py --all
+ backfill_validation_flags.py) that brings the corpus to consistency.

Usage:
  python3 scripts/audit_corpus_completeness.py            # report only
  python3 scripts/audit_corpus_completeness.py --fix      # also execute fix
  python3 scripts/audit_corpus_completeness.py --verbose  # per-case detail
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WEBAPP = ROOT / 'webapp'
SCRIPTS = ROOT / 'scripts'

# Fields written by run_network_full_corrections.py during a successful
# Stage E pass.  Listed in dependency order so the report can tell the
# user *why* downstream fields are missing.
STAGE_E_KEYS = [
    'sigma_full_mScm_stage_e',
    'electronic_sigma_full_mScm_stage_e',
    'thermal_sigma_full_mScm_stage_e',
]
STAGE_E_AUDIT_KEYS = [
    'stage_e_source',          # which channels direct-solved vs fallback'd
    'stage_e_factors_used',    # audit trail of Cronau / Trev. / Wang factors
]
BASELINE_KEYS = [
    'sigma_full_mScm',                  # σ_ionic baseline
    'electronic_sigma_full_mScm',       # σ_e baseline
    'thermal_sigma_full_mScm',          # κ baseline
]


def discover_cases() -> list[Path]:
    seen: set[Path] = set()
    out: list[Path] = []
    for base in ('archive', 'results'):
        root = WEBAPP / base
        if not root.exists():
            continue
        for fm in root.rglob('full_metrics.json'):
            d = fm.parent
            if d not in seen:
                seen.add(d)
                out.append(d)
    return sorted(out)


def _present(fm: dict, key: str) -> bool:
    """A key is 'present' if it exists and is neither None nor empty."""
    v = fm.get(key)
    if v is None:
        return False
    if isinstance(v, (dict, list)) and not v:
        return False
    return True


def _classify(fm: dict) -> tuple[str, list[str]]:
    """Return (category, list_of_missing_fields) for a single case."""
    missing = []

    # Stage E channels
    for k in STAGE_E_KEYS:
        if not _present(fm, k):
            missing.append(k)

    # Stage E audit trail
    if not _present(fm, 'stage_e_source'):
        missing.append('stage_e_source')

    # Validation flags self-report
    flags = fm.get('validation_flags')
    if not isinstance(flags, dict) or not flags:
        missing.append('validation_flags')

    # Baseline sanity
    baseline_missing = [k for k in BASELINE_KEYS if not _present(fm, k)]
    if len(baseline_missing) == len(BASELINE_KEYS):
        return 'no-baseline', missing + baseline_missing

    # Categorise
    stage_e_missing = [k for k in STAGE_E_KEYS if k in missing]
    if not stage_e_missing and 'validation_flags' not in missing:
        return 'complete', []
    if not stage_e_missing and 'validation_flags' in missing:
        return 'no-validation-flags', ['validation_flags']
    if len(stage_e_missing) == len(STAGE_E_KEYS):
        return 'no-stage-e', missing
    return 'partial-stage-e', missing


CAT_ORDER = [
    'no-baseline',
    'no-stage-e',
    'partial-stage-e',
    'no-validation-flags',
    'complete',
]
CAT_ICON = {
    'complete':            '✓',
    'partial-stage-e':     '~',
    'no-stage-e':          '⚠',
    'no-validation-flags': '⚠',
    'no-baseline':         '✗',
}


def main() -> None:
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--fix', action='store_true',
                     help='Execute the suggested fix commands after audit')
    ap.add_argument('--verbose', '-v', action='store_true',
                     help='Print per-case missing fields')
    args = ap.parse_args()

    cases = discover_cases()
    if not cases:
        print('No cases found under webapp/archive or webapp/results.')
        sys.exit(0)

    print(f'\n=== Corpus completeness audit ({len(cases)} cases) ===\n')

    by_cat: dict[str, list[tuple[Path, list[str]]]] = {c: [] for c in CAT_ORDER}
    for d in cases:
        try:
            fm = json.loads((d / 'full_metrics.json').read_text())
        except (OSError, ValueError):
            by_cat['no-baseline'].append((d, ['<full_metrics.json malformed>']))
            continue
        cat, missing = _classify(fm)
        by_cat[cat].append((d, missing))

    for cat in CAT_ORDER:
        items = by_cat[cat]
        if not items:
            continue
        icon = CAT_ICON[cat]
        print(f'{icon} {cat}  ({len(items)} cases)')
        if args.verbose or cat in ('no-baseline', 'partial-stage-e'):
            for d, missing in items[:30]:
                src_case = d.name
                if missing:
                    short = ', '.join(missing[:4])
                    if len(missing) > 4:
                        short += f', +{len(missing) - 4} more'
                    print(f'    {src_case:35s}  missing: {short}')
                else:
                    print(f'    {src_case}')
            if len(items) > 30:
                print(f'    … and {len(items) - 30} more')
        print()

    # Build fix command
    need_stage_e = [d for d, _ in by_cat['no-stage-e']
                          + by_cat['partial-stage-e']]
    need_backfill = [d for d, _ in by_cat['no-validation-flags']]

    if not (need_stage_e or need_backfill):
        print('Everything up to date — no fix needed.')
        return

    print('=== Suggested fix ===\n')
    cmds: list[list[str]] = []
    if need_stage_e:
        # Use find_and_rerun_stage_e.py --all to rerun Stage E on every
        # case (handles the partial-stage-e cases too — the worker is
        # idempotent and rewrites all three channels).
        print(f'1. Re-run Stage E on {len(need_stage_e)} cases:')
        print(f'   python3 scripts/find_and_rerun_stage_e.py --all\n')
        cmds.append([sys.executable, str(SCRIPTS / 'find_and_rerun_stage_e.py'),
                       '--all'])
    if need_backfill or need_stage_e:
        # backfill is cheap to always run after Stage E.
        print(f'2. Backfill validation_flags self-report card:')
        print(f'   python3 scripts/backfill_validation_flags.py\n')
        cmds.append([sys.executable,
                       str(SCRIPTS / 'backfill_validation_flags.py')])

    if not args.fix:
        print('Pass --fix to execute these commands now.')
        return

    print('--- Executing fix ---\n')
    for cmd in cmds:
        print(f'$ {" ".join(cmd)}')
        cp = subprocess.run(cmd)
        if cp.returncode != 0:
            print(f'  ✗ exit {cp.returncode}, stopping.')
            sys.exit(cp.returncode)
    print('\nFix complete. Re-run this audit to confirm corpus is clean.')


if __name__ == '__main__':
    main()
