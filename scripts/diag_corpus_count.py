#!/usr/bin/env python3
"""Trace where cases drop between disk corpus (~113) and form corpus (97).

Reports per-filter counts:
  1. cases on disk
  2. cases loaded (excluded if not 'input_' prefix or no name)
  3. cases with raw σ_e > 0 (Stage E)
  4. cases passing form filter (all metrics > 0)
  5. cases in form arr (after dedup by name)
  6. cases excluded from fit (in _EXCLUDED_NAMES_EL)
  7. cases used in fit (n_fit)
"""
import sys, json, glob
from pathlib import Path
sys.path.insert(0, 'scripts')
import generate_comparison_plots as gcp


def main():
    # Step 1-2: walk disk
    disk_files = sorted(glob.glob('webapp/archive/**/full_metrics.json', recursive=True))
    print(f"Step 1: full_metrics.json files on disk: {len(disk_files)}")

    loaded = []
    seen_names = set()
    for f in disk_files:
        nm = Path(f).parent.name
        meta_p = Path(f).parent / 'meta.json'
        if meta_p.exists():
            try:
                mn = json.load(open(meta_p)).get('name', '') or ''
                if mn: nm = mn
            except: pass
        if not nm.startswith('input_'):
            continue
        if nm in seen_names:
            continue
        seen_names.add(nm)
        try:
            d = json.load(open(f))
            loaded.append((nm, d, f))
        except Exception as e:
            print(f"  [load err] {nm}: {e}")
    print(f"Step 2: loaded (input_*, dedup by name): {len(loaded)}")
    skipped_load = len(disk_files) - len(loaded)
    print(f"  → skipped at load step: {skipped_load}")

    # Step 3: σ_e > 0
    with_sig = []
    no_sig = []
    for nm, d, f in loaded:
        sig = (d.get('electronic_sigma_full_mScm_stage_e') or
               d.get('electronic_sigma_full_mScm') or 0)
        if sig and sig > 0:
            with_sig.append((nm, d, f, sig))
        else:
            no_sig.append((nm, d, f, sig))
    print(f"\nStep 3: cases with σ_e > 0 (Stage E or raw): {len(with_sig)}")
    print(f"  → cases with σ_e = 0 or None: {len(no_sig)}")
    if no_sig:
        for nm, _, _, sig in no_sig[:10]:
            print(f"     {nm}  σ_e={sig}")
        if len(no_sig) > 10:
            print(f"     ... +{len(no_sig)-10} more")

    # Step 4: form filter — strict pass
    data_list = [d for _, d, _ in loaded]
    names_list = [nm for nm, _, _ in loaded]
    arr_strict = gcp._electronic_form_arrays(data_list, names_list)
    if arr_strict is None:
        print(f"\nStep 4: ABORT — arr_strict None")
        return
    n_strict = arr_strict['n']
    print(f"\nStep 4: form arr (strict pass, σ_e required): {n_strict}")
    in_strict_names = set(arr_strict['names'])

    # Show what dropped from loaded → strict
    dropped_at_strict = [nm for nm, _, _ in loaded if nm not in in_strict_names]
    print(f"  → dropped from form strict filter: {len(dropped_at_strict)}")
    if dropped_at_strict:
        print(f"     (filter blocks: phi_am≤0.30, am_am_cn=0, coverage=0, f_perc=0, tau=0, am_area=0, sig=0)")
        for nm in dropped_at_strict[:15]:
            d = next(x[1] for x in loaded if x[0] == nm)
            sig = (d.get('electronic_sigma_full_mScm_stage_e') or
                   d.get('electronic_sigma_full_mScm') or 0)
            phi = d.get('phi_am', 0) or 0
            cn = d.get('am_am_cn', 0) or 0
            cov_p = d.get('coverage_AM_P_mean', 0) or 0
            cov_s = d.get('coverage_AM_S_mean', 0) or 0
            fp = (d.get('electronic_percolating_fraction') or
                  (d.get('percolation_pct') or 0) / 100.0)
            am_area = d.get('am_am_mean_area', 0) or 0
            tau = (d.get('tortuosity_electronic_recommended') or
                   d.get('tortuosity_electronic_mean') or 0)
            reasons = []
            if not (sig and sig > 0): reasons.append(f'σ={sig}')
            if not (phi and phi > 0.30): reasons.append(f'φ={phi:.3f}')
            if not (cn and cn > 0): reasons.append(f'CN={cn}')
            if not ((cov_p > 0) or (cov_s > 0)): reasons.append(f'cov_P={cov_p},S={cov_s}')
            if not (fp and fp > 0): reasons.append(f'f_p={fp}')
            if not (am_area and am_area > 0): reasons.append(f'A={am_area}')
            if not (tau and tau > 0): reasons.append(f'τ={tau}')
            print(f"     {nm:35s}  {', '.join(reasons)}")
        if len(dropped_at_strict) > 15:
            print(f"     ... +{len(dropped_at_strict)-15} more")

    # Step 5-6: EXCL and fit
    excl_mask = arr_strict['excluded']
    n_excl = int(excl_mask.sum())
    n_fit = n_strict - n_excl
    print(f"\nStep 5: in form arr (n_strict): {n_strict}")
    print(f"Step 6: AUDIT EXCLUDED (in _EXCLUDED_NAMES_EL): {n_excl}")
    print(f"Step 7: in fit (n_fit = n_strict - n_excl): {n_fit}")

    print()
    print("=" * 80)
    print(f"  SUMMARY: disk_files={len(disk_files)} → loaded={len(loaded)}")
    print(f"           → arr_strict={n_strict} → fit={n_fit}")
    print(f"  Missing from form: {len(loaded) - n_strict}")


if __name__ == '__main__':
    main()
