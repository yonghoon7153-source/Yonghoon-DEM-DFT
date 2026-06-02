#!/usr/bin/env python3
"""B-1: Recompute missing coverage_AM_mean and f_perc_x_AM for older sims
that have raw σ_e but are filtered out of σ_e form arrays.

Identified 31 cases (mostly older 1mAh_100_X sims, 1mAh_9_S*, 1mAh_8_S*,
1mAh_8_AMP_S*, 1mAh_5_AMP_S4/5, particulate_1/4, S_1) that:
  - have raw σ_e (network solver ran successfully)
  - LACK cov_AM_mean (Hertz coverage) and/or f_perc_x_AM (percolation)
  - thus filtered from _electronic_form_arrays → no form prediction

This script:
  1. Walks webapp/archive + webapp/results
  2. Identifies cases missing the 2 metrics
  3. For each, attempts to compute from available particle/network data:
       coverage_AM_mean = (sum of Hertz AM-AM contact areas / total AM area) × 100
       f_perc_x_AM = fraction of AM that percolates in x-direction
  4. Writes updated full_metrics.json (with backup)

Run on WSL:
    python3 scripts/recompute_missing_metrics.py --dry-run    # preview
    python3 scripts/recompute_missing_metrics.py              # apply

Notes:
  - Requires atoms.csv (particle positions/radii) and network_conductivity.json
    (Hertz contact data) per case
  - If those are absent (e.g., archive-only cases), prints case as skipped
  - Backup created as full_metrics.json.bak before modification
"""
from __future__ import annotations
import sys, json, argparse, shutil
from pathlib import Path
import numpy as np


def find_cases_missing_metrics(roots):
    """Return list of (case_dir, metrics_dict, missing_fields)."""
    out = []
    for root in roots:
        rp = Path(root)
        if not rp.is_dir(): continue
        for mp in rp.rglob('full_metrics.json'):
            try:
                d = json.load(open(mp))
            except: continue
            missing = []
            if not d.get('coverage_AM_mean'):
                missing.append('coverage_AM_mean')
            if not d.get('f_perc_x_AM'):
                missing.append('f_perc_x_AM')
            if not missing:
                continue
            # Only target cases with VALID raw σ_e (solver did run)
            sig = d.get('electronic_sigma_full_mScm') or d.get('electronic_sigma_full_mScm_stage_e')
            if not (sig and sig > 0):
                continue
            out.append((mp.parent, d, missing))
    return out


def compute_coverage_AM(case_dir):
    """coverage_AM_mean (%) = total Hertz AM-AM contact area / total AM surface × 100.
    Falls back to looking at network_conductivity.json contact list."""
    nc_path = case_dir / 'network_conductivity.json'
    if not nc_path.exists():
        return None
    try:
        nc = json.load(open(nc_path))
    except: return None
    # Try multiple possible structures
    contacts = nc.get('contacts') or nc.get('am_am_contacts') or []
    total_area = 0.0
    for c in contacts:
        if not isinstance(c, dict): continue
        a = c.get('area_um2') or c.get('hertz_area') or c.get('area')
        # Filter to AM-AM only if type info available
        ct = c.get('type', 'AM-AM').upper()
        if 'AM' in ct and a and a > 0:
            total_area += float(a)
    if total_area <= 0: return None
    # AM surface estimate from particle radii
    atoms_path = case_dir / 'atoms.csv'
    if atoms_path.exists():
        try:
            radii = []
            import csv
            with open(atoms_path) as f:
                rdr = csv.DictReader(f)
                for row in rdr:
                    t = (row.get('type') or '').upper()
                    if 'AM' in t:
                        r = float(row.get('radius_um') or row.get('r') or 0)
                        if r > 0: radii.append(r)
            if radii:
                am_surf = sum(4*np.pi*r*r for r in radii)
                return float(total_area / am_surf * 100)
        except: pass
    return None


def compute_f_perc_x_AM(case_dir):
    """f_perc_x_AM = fraction of AM particles in the x-percolating cluster."""
    nc_path = case_dir / 'network_conductivity.json'
    if not nc_path.exists():
        return None
    try:
        nc = json.load(open(nc_path))
    except: return None
    # Try direct field first
    for k in ('f_perc_x_AM', 'f_perc_AM_x', 'percolation_fraction_x_AM',
              'percolation_x_AM', 'f_perc_x'):
        v = nc.get(k)
        if isinstance(v, (int, float)) and 0 <= v <= 1:
            return float(v)
        if isinstance(v, (int, float)) and 0 <= v <= 100:
            return float(v) / 100
    # Try percolation_pct (generic)
    v = nc.get('percolation_pct') or nc.get('percolating_fraction_pct')
    if isinstance(v, (int, float)) and 0 <= v <= 100:
        return float(v) / 100
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dry-run', action='store_true', help="Preview without writing")
    ap.add_argument('--roots', nargs='+', default=['webapp/archive', 'webapp/results'])
    args = ap.parse_args()

    cases = find_cases_missing_metrics(args.roots)
    print(f"Found {len(cases)} cases with raw σ_e but missing form metrics")
    print()

    fixed_cov = 0; fixed_fp = 0; both = 0; skipped = 0
    for case_dir, d, missing in cases:
        name = case_dir.name
        meta = case_dir / 'meta.json'
        nm = name
        if meta.exists():
            try: nm = json.load(open(meta)).get('name', name) or name
            except: pass
        print(f"  {nm[:40]:40s}  missing: {','.join(missing)}")
        updated = False
        new = dict(d)  # shallow copy
        if 'coverage_AM_mean' in missing:
            v = compute_coverage_AM(case_dir)
            if v is not None and v > 0:
                new['coverage_AM_mean'] = v
                fixed_cov += 1
                print(f"      → coverage_AM_mean = {v:.2f}%")
                updated = True
            else:
                print(f"      → coverage_AM_mean: cannot compute (network_conductivity.json missing or no AM contacts)")
        if 'f_perc_x_AM' in missing:
            v = compute_f_perc_x_AM(case_dir)
            if v is not None and 0 <= v <= 1:
                new['f_perc_x_AM'] = v
                fixed_fp += 1
                print(f"      → f_perc_x_AM = {v:.3f}")
                updated = True
            else:
                print(f"      → f_perc_x_AM: cannot compute (network field absent)")
        if updated:
            if 'coverage_AM_mean' not in missing or new.get('coverage_AM_mean'):
                if 'f_perc_x_AM' not in missing or new.get('f_perc_x_AM'):
                    both += 1
            if not args.dry_run:
                bak = case_dir / 'full_metrics.json.bak'
                if not bak.exists():
                    shutil.copy(case_dir / 'full_metrics.json', bak)
                with open(case_dir / 'full_metrics.json', 'w') as f:
                    json.dump(new, f, indent=2, ensure_ascii=False)
                print(f"      ✓ written to disk (backup: full_metrics.json.bak)")
            else:
                print(f"      [DRY-RUN] would write to disk")
        else:
            skipped += 1
    print()
    print(f"Summary:")
    print(f"  cases inspected:      {len(cases)}")
    print(f"  coverage_AM filled:   {fixed_cov}")
    print(f"  f_perc_x_AM filled:   {fixed_fp}")
    print(f"  fully fixed (both):   {both}")
    print(f"  skipped (no source):  {skipped}")
    if args.dry_run:
        print()
        print("This was a DRY-RUN.  Re-run WITHOUT --dry-run to apply changes.")


if __name__ == '__main__':
    main()
