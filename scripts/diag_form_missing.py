#!/usr/bin/env python3
"""Identify cases where σ_e raw exists but form prediction fails (gray squares
in σ_e plots).  Mirrors _electronic_form_arrays filter logic exactly.

Usage: python3 scripts/diag_form_missing.py
"""
import json, glob
from pathlib import Path

_PHI_AM_MIN = 0.30


def _f_perc_e_target(d):
    """Mirror generate_comparison_plots._f_perc_e_target."""
    v = d.get('electronic_percolating_fraction')
    if isinstance(v, (int, float)) and v > 0:
        return float(v)
    v = d.get('percolation_pct')
    return float(v) / 100.0 if isinstance(v, (int, float)) and v > 0 else None


def _cov_val(d):
    """Form needs coverage > 0 (uses either P or S mean)."""
    for k in ('coverage_AM_P_mean', 'coverage_AM_S_mean'):
        v = d.get(k)
        if isinstance(v, (int, float)) and v > 0: return v
    return None


def _tau_val(d):
    for k in ('tortuosity_electronic_recommended',
             'tortuosity_electronic_mean',
             'tortuosity_recommended', 'tortuosity_mean'):
        v = d.get(k)
        if isinstance(v, (int, float)) and v > 0: return v
    return None


CHECKS = [
    ('phi_am > 0.30',       lambda d: (d.get('phi_am') or 0) > _PHI_AM_MIN),
    ('am_am_cn > 0',        lambda d: (d.get('am_am_cn') or 0) > 0),
    ('coverage_AM > 0',     lambda d: _cov_val(d) is not None),
    ('f_perc > 0',          lambda d: _f_perc_e_target(d) is not None),
    ('tau > 0',             lambda d: _tau_val(d) is not None),
    ('am_am_mean_area > 0', lambda d: (d.get('am_am_mean_area') or 0) > 0),
]


def has_raw_sigma_e(d):
    for k in ('electronic_sigma_full_mScm_stage_e',
              'electronic_sigma_full_mScm',
              'electronic_sigma_full_mScm_stage_e_physics',
              'electronic_sigma_full_mScm_physics'):
        v = d.get(k)
        if v is not None and v > 0: return v
    return None


cases = []
for f in glob.glob('webapp/archive/**/full_metrics.json', recursive=True):
    try:
        d = json.load(open(f))
    except: continue
    sig = has_raw_sigma_e(d)
    if sig is None: continue
    missing = [(lbl, getter) for lbl, getter in CHECKS if not getter(d)]
    if missing:
        name = Path(f).parent.name
        # also report the raw values for missing metrics
        details = []
        for lbl, getter in missing:
            if 'phi_am' in lbl:        details.append(f'phi_am={d.get("phi_am")}')
            elif 'am_am_cn' in lbl:    details.append(f'am_am_cn={d.get("am_am_cn")}')
            elif 'coverage' in lbl:    details.append(f'cov_P={d.get("coverage_AM_P_mean")}, cov_S={d.get("coverage_AM_S_mean")}')
            elif 'f_perc' in lbl:      details.append(f'percolation_pct={d.get("percolation_pct")}, elec_perc_frac={d.get("electronic_percolating_fraction")}')
            elif 'tau' in lbl:         details.append(f'tau_elec_rec={d.get("tortuosity_electronic_recommended")}')
            elif 'am_am_mean_area' in lbl: details.append(f'am_am_area={d.get("am_am_mean_area")}')
        cases.append((name, sig, [lbl for lbl, _ in missing], details))

print(f"=== Cases with raw σ_e but form-blocking metric (real) ({len(cases)} total) ===\n")
if not cases:
    print("  ALL CASES PASS form filter — no gray squares should appear in plots.")
else:
    for name, sig, missing_lbls, details in cases:
        print(f"  {name:35s}  σ_e={sig:.2f}")
        for lbl, det in zip(missing_lbls, details):
            print(f"    ✗ {lbl}  ({det})")
