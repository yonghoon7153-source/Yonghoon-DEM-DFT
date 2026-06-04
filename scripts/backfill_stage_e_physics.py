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

    # PRESERVE existing Hertz Stage E values — run_network_full_corrections.py
    # recomputes ALL Stage E channels (Hertz + Physics), but its Hertz σ_e
    # output can differ from the validated production values (fracture factor
    # over-application observed 2026-06-04: σ_e Hertz Stage E compressed 5-6×).
    # We only WANT the new Physics Stage E; the Hertz Stage E must stay as-is.
    # Snapshot Hertz Stage E before, restore after.
    HERTZ_KEYS = ['electronic_sigma_full_mScm_stage_e',
                  'sigma_full_mScm_stage_e',
                  'thermal_sigma_full_mScm_stage_e']
    snapshot = {}   # case_name → {key: value}
    for nm in names:
        for base in ('webapp/archive', 'webapp/results'):
            fp = list(Path(base).rglob(f'{nm}/full_metrics.json'))
            if fp:
                try:
                    d = json.load(open(fp[0]))
                    snapshot[nm] = {k: d.get(k) for k in HERTZ_KEYS if d.get(k)}
                except: pass
                break

    print(f"\nInvoking run_network_full_corrections.py on {len(names)} cases...\n")
    cmd = ['python3', 'scripts/run_network_full_corrections.py', '--quiet'] + names
    subprocess.run(cmd)

    # Restore Hertz Stage E from snapshot (keep new Physics Stage E)
    n_restored = 0
    for nm, saved in snapshot.items():
        if not saved: continue
        for base in ('webapp/archive', 'webapp/results'):
            fp = list(Path(base).rglob(f'{nm}/full_metrics.json'))
            if fp:
                try:
                    d = json.load(open(fp[0]))
                    changed = False
                    for k, v in saved.items():
                        if v and d.get(k) != v:
                            d[k] = v; changed = True
                    if changed:
                        json.dump(d, open(fp[0], 'w'), indent=2, ensure_ascii=False)
                        n_restored += 1
                except: pass
                break
    print(f"  Restored Hertz Stage E in {n_restored} cases (preserved production values)")

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
