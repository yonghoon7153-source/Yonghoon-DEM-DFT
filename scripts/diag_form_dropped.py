#!/usr/bin/env python3
"""Run _electronic_form_arrays on full corpus and report which cases drop, why.
Specifically targets the 1mAh_8_AMP_S* family to find why they're 'form unavailable'.

Usage: python3 scripts/diag_form_dropped.py
"""
import json, glob, sys
from pathlib import Path
sys.path.insert(0, 'scripts')

import generate_comparison_plots as gcp


def find_all_cases():
    data_list, names = [], []
    for f in sorted(glob.glob('webapp/archive/**/full_metrics.json', recursive=True)):
        try:
            d = json.load(open(f))
        except: continue
        meta_p = Path(f).parent / 'meta.json'
        nm = Path(f).parent.name
        if meta_p.exists():
            try:
                mn = json.load(open(meta_p)).get('name', '') or ''
                if mn: nm = mn
            except: pass
        if nm in [n for n in names]: continue  # dedup by name
        data_list.append(d); names.append(nm)
    return data_list, names


def main():
    data_list, names = find_all_cases()
    print(f"Total cases loaded: {len(data_list)}\n")

    # Run strict pass
    arr = gcp._electronic_form_arrays(data_list, names)
    if arr is None:
        print("ABORT: _electronic_form_arrays returned None")
        return

    kept = set(int(i) for i in arr['keep_idx'])
    print(f"Kept by strict pass: {len(kept)}")
    dropped = [i for i in range(len(data_list)) if i not in kept]
    print(f"Dropped (any reason): {len(dropped)}\n")

    # Run relaxed pass
    arr_inc = gcp._electronic_form_arrays(data_list, names, allow_no_sigma=True)
    kept_inc = set(int(i) for i in arr_inc['keep_idx']) if arr_inc is not None else set()
    in_either = kept | kept_inc
    truly_dropped = [i for i in dropped if i not in in_either]
    print(f"Dropped by BOTH passes (truly unavailable): {len(truly_dropped)}\n")

    # Report all dropped
    print(f"{'#':>3} {'name':35s} {'σ_e':>8s} {'reason'}")
    for i in dropped:
        d = data_list[i]; nm = names[i]
        sig = (d.get('electronic_sigma_full_mScm_stage_e') or
               d.get('electronic_sigma_full_mScm') or 0)
        # Diagnose why dropped
        reasons = []
        phi = d.get('phi_am') or 0
        cn = d.get('am_am_cn') or 0
        cov = max(d.get('coverage_AM_P_mean', 0) or 0,
                  d.get('coverage_AM_S_mean', 0) or 0)
        fp = gcp._f_perc_e_target(d)
        tau = None
        for k in ('tortuosity_electronic_recommended','tortuosity_electronic_mean',
                  'tortuosity_recommended','tortuosity_mean'):
            v = d.get(k)
            if isinstance(v, (int, float)) and v > 0: tau = v; break
        am_area = d.get('am_am_mean_area') or 0

        if phi <= gcp._PHI_AM_MIN: reasons.append(f'phi_am={phi:.3f}≤0.30')
        if not (cn and cn > 0): reasons.append(f'am_am_cn={cn}')
        if not (cov and cov > 0): reasons.append('coverage=0')
        if not (fp and fp > 0): reasons.append(f'f_perc={fp}')
        if not (tau and tau > 0): reasons.append(f'tau={tau}')
        if not (am_area and am_area > 0): reasons.append(f'am_area={am_area}')
        if sig <= 0: reasons.append(f'σ_e={sig}')

        if not reasons:
            # Check dedup: was another case with same key kept?
            key = (round(float(phi), 4), round(float(cn), 3), round(float(sig), 5))
            collide = []
            for j in kept:
                dj = data_list[j]
                phi_j = dj.get('phi_am') or 0; cn_j = dj.get('am_am_cn') or 0
                sj = (dj.get('electronic_sigma_full_mScm_stage_e') or
                      dj.get('electronic_sigma_full_mScm') or 0)
                key_j = (round(float(phi_j), 4), round(float(cn_j), 3), round(float(sj), 5))
                if key_j == key:
                    collide.append(names[j])
            if collide:
                reasons.append(f'DEDUP (key collides with {collide[0]})')
            else:
                reasons.append('UNKNOWN — strict filter passed but not kept')

        in_inc = i in kept_inc
        flag = '[recovered by relaxed pass]' if in_inc else '✗ TRULY DROPPED'
        print(f"{i:>3d} {nm[:35]:35s} {sig:>8.2f}  {', '.join(reasons)} {flag}")


if __name__ == '__main__':
    main()
