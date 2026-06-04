#!/usr/bin/env python3
"""Backfill Stage E Physics fields for cases that have Hertz Stage E but
not Physics Stage E.

These are typically cases analyzed before physics-mode Stage E was added
to run_network_full_corrections.py, or where physics-mode silently failed.

Walks all webapp/archive cases, identifies missing Stage E Physics, and
re-runs run_network_full_corrections.py on them.

Usage:
    python3 scripts/backfill_stage_e_physics.py [--dry-run]
"""
import sys, json, glob, subprocess
from pathlib import Path


def find_incomplete():
    """Return case names that have Hertz Stage E but missing Physics Stage E.
    Scans BOTH webapp/archive AND webapp/results — these are the two places
    where full_metrics.json lives (results = live cases, archive = saved)."""
    incomplete = []
    seen = set()
    for base in ('webapp/archive', 'webapp/results'):
        for f in sorted(glob.glob(f'{base}/**/full_metrics.json', recursive=True)):
            nm = Path(f).parent.name
            if nm in seen: continue
            try: d = json.load(open(f))
            except: continue
            # Has Hertz Stage E (production)?
            has_hertz = any(d.get(k) for k in (
                'sigma_full_mScm_stage_e',
                'electronic_sigma_full_mScm_stage_e',
                'thermal_sigma_full_mScm_stage_e'))
            # Missing any Physics Stage E?
            missing = [k for k in (
                'sigma_full_mScm_stage_e_physics',
                'electronic_sigma_full_mScm_stage_e_physics',
                'thermal_sigma_full_mScm_stage_e_physics') if not d.get(k)]
            if has_hertz and missing:
                incomplete.append((nm, missing))
                seen.add(nm)
            else:
                seen.add(nm)
    return incomplete


def main():
    dry_run = '--dry-run' in sys.argv
    incomplete = find_incomplete()
    print(f"\nCases with Hertz Stage E but missing Physics Stage E: {len(incomplete)}\n")
    if not incomplete:
        print("  ✓ All cases complete.  No action needed.")
        return
    print(f"  {'Case':40s}  Missing Physics-Stage-E channels")
    for nm, missing in incomplete[:30]:
        labels = [m.replace('_stage_e_physics', '').replace('_full_mScm', '')
                   .replace('electronic_sigma', 'σ_e').replace('thermal_sigma', 'κ')
                   .replace('sigma', 'σ_ionic') for m in missing]
        print(f"  {nm:40s}  {', '.join(labels)}")
    if len(incomplete) > 30:
        print(f"  ... +{len(incomplete)-30} more")
    print()
    if dry_run:
        print("  --dry-run: showing only.  Run without --dry-run to invoke "
              "run_network_full_corrections.py")
        return
    names = [nm for nm, _ in incomplete]
    print(f"\nInvoking run_network_full_corrections.py on {len(names)} cases...\n")
    cmd = ['python3', 'scripts/run_network_full_corrections.py', '--quiet'] + names
    subprocess.run(cmd)
    # Verify
    print("\n── Verification ──")
    still_missing = find_incomplete()
    print(f"  After backfill: {len(still_missing)} cases still incomplete "
          f"(was {len(incomplete)})")
    if still_missing:
        for nm, m in still_missing[:10]:
            print(f"    ✗ {nm}: {[x.replace('_stage_e_physics','').replace('_full_mScm','') for x in m]}")


if __name__ == '__main__':
    main()
