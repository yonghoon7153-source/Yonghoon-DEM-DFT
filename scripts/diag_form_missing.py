#!/usr/bin/env python3
"""Identify cases where σ_e raw exists but form prediction fails (gray squares
in σ_e plots).  Reports which metric is missing per case so user can decide:
  - re-run analysis pipeline to recover (if metric is computable)
  - leave as-is (if metric truly cannot be derived from this case)

Usage: python3 scripts/diag_form_missing.py
"""
import json, glob
from pathlib import Path

# Match _electronic_form_arrays filter conditions
REQUIRED = [
    ('phi_am',                              lambda d: d.get('phi_am'),                              'phi_am > 0.30'),
    ('am_am_cn',                            lambda d: d.get('am_am_cn'),                            '> 0'),
    ('coverage (P or S)',                   lambda d: max(d.get('coverage_AM_P_mean', 0) or 0,
                                                          d.get('coverage_AM_S_mean', 0) or 0),     '> 0'),
    ('f_perc_x_AM',                         lambda d: d.get('f_perc_x_AM') or d.get('f_perc_recommended'), '> 0'),
    ('tortuosity_electronic',               lambda d: (d.get('tortuosity_electronic_recommended') or
                                                       d.get('tortuosity_electronic_mean') or
                                                       d.get('tortuosity_recommended') or
                                                       d.get('tortuosity_mean')),                   '> 0'),
    ('am_am_mean_area',                     lambda d: d.get('am_am_mean_area'),                     '> 0'),
]

def has_raw_sigma_e(d):
    for k in ('electronic_sigma_full_mScm_stage_e',
              'electronic_sigma_full_mScm',
              'electronic_sigma_full_mScm_stage_e_physics',
              'electronic_sigma_full_mScm_physics'):
        v = d.get(k)
        if v is not None and v > 0:
            return v
    return None

cases_missing = []
for f in glob.glob('webapp/archive/**/full_metrics.json', recursive=True):
    try:
        d = json.load(open(f))
    except: continue
    sig = has_raw_sigma_e(d)
    if sig is None: continue
    missing = []
    for lbl, getter, _ in REQUIRED:
        v = getter(d)
        ok = (v is not None and isinstance(v, (int, float)) and v > 0
              and (v > 0.30 if lbl == 'phi_am' else True))
        if not ok:
            missing.append((lbl, v))
    if missing:
        name = Path(f).parent.name
        cases_missing.append((name, sig, missing))

print(f"=== Cases with raw σ_e but form-blocking metric missing ({len(cases_missing)} total) ===\n")
for name, sig, missing in cases_missing:
    miss_str = ', '.join(f'{lbl}={v}' for lbl, v in missing)
    print(f"  {name:35s}  σ_e_raw={sig:.2f}  MISSING: {miss_str}")
