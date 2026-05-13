#!/usr/bin/env python3
"""Populate full_metrics.json with the Stage-E `validation_flags`
self-report card without re-running the network solver.

Useful when:
  * the archive contains old cases whose Stage E predates the flag-
    writing patch in run_network_full_corrections.py;
  * the user just wants to audit which cases are within the
    Bielefeld/Lee experimental window for a paper figure;
  * the flag definition changes and we want to re-stamp without
    spsolve cost.

Reuses _compute_validation_flags from run_network_full_corrections to
keep a single source of truth.

Usage:
  python3 scripts/backfill_validation_flags.py             # all cases
  python3 scripts/backfill_validation_flags.py <case_id...>  # subset
"""
from __future__ import annotations
import json
import sys
from pathlib import Path

ROOT    = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / 'scripts'
WEBAPP  = ROOT / 'webapp'

sys.path.insert(0, str(SCRIPTS))
from run_network_full_corrections import (         # noqa: E402
    _compute_validation_flags, discover_case_dirs,
)


def main() -> None:
    wanted = {Path(c).name for c in sys.argv[1:]}
    cases  = discover_case_dirs()
    if wanted:
        cases = [d for d in cases if d.name in wanted]
    if not cases:
        print('No cases found.', flush=True); sys.exit(1)

    n_ok = n_skip = n_pass = 0
    for d in cases:
        fm_p = d / 'full_metrics.json'
        try:
            fm = json.loads(fm_p.read_text())
        except Exception as e:
            print(f'  ✗ {d.name}: cannot read full_metrics.json — {e}')
            n_skip += 1
            continue
        # Reconstruct the inputs the flag computer expects from what
        # Stage E persisted last time.  When fields are missing the
        # helper conservatively returns None for that gate.
        factors = {
            'fracture_stage_counts': fm.get('stage_e_fracture_stage_counts') or {},
            'n_dropped_e':           (fm.get('stage_e_factors_used') or {}).get('n_dropped_e'),
            'n_am_am_total':         (fm.get('stage_e_factors_used') or {}).get('n_am_am_total'),
        }
        flags = _compute_validation_flags(
            fm, factors,
            fm.get('sigma_full_mScm_stage_e'),
            fm.get('electronic_sigma_full_mScm_stage_e'),
            fm.get('thermal_sigma_full_mScm_stage_e'),
        )
        fm['validation_flags'] = flags
        with open(fm_p, 'w') as f:
            json.dump(fm, f, indent=2, default=str)
        n_ok += 1
        if flags.get('trustworthy_overall'): n_pass += 1
        tag = '✓' if flags.get('trustworthy_overall') else '·'
        print(f'  {tag} {d.name:32s}  '
              f'ASR={flags.get("asr_ionic_Ohm_cm2")}  '
              f'severe={flags.get("fracture_severe_pct")}%')

    print(f'\nDone — flagged {n_ok} cases ({n_pass} fully trustworthy, '
          f'{n_skip} skipped).', flush=True)


if __name__ == '__main__':
    main()
