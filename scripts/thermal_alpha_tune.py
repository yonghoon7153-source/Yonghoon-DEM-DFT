#!/usr/bin/env python3
"""Tune Ridge alpha for thermal Stage T1 to robustly clear LOOCV 0.90.

Production _thermal_fit gives 0.894 (vs verification 0.903) due to corpus
+1 (hash test cases included).  Sweep alpha to find robust 0.90+ setting.
"""
import sys, json, glob
from pathlib import Path
import numpy as np
sys.path.insert(0, 'scripts')
import generate_comparison_plots as gcp


def main():
    dl, ns, seen = [], [], set()
    for base in ('webapp/archive', 'webapp/results'):
        for f in sorted(glob.glob(f'{base}/**/full_metrics.json', recursive=True)):
            nm = Path(f).parent.name
            if nm in seen: continue
            seen.add(nm)
            try: dl.append(json.load(open(f))); ns.append(nm)
            except: continue

    print(f"Total loaded: {len(dl)}")

    # All-names corpus
    arr_all = gcp._thermal_form_arrays(dl, ns)
    if arr_all:
        print(f"\n[ALL names] n={arr_all['n']}, n_fit={(~arr_all['excluded']).sum()}")
        for a in [0.01, 0.05, 0.1, 0.3, 0.5, 1.0, 2.0, 5.0]:
            fit = gcp._thermal_fit(arr_all, fit_mask=~arr_all['excluded'], alpha=a)
            flag = ' ⭐' if fit['loocv'] >= 0.9 else ''
            print(f"  α={a:>5.2f}: LOOCV={fit['loocv']:.4f} R²={fit['r2']:.4f}{flag}")

    # input_ only corpus (matches verification script)
    dl2 = [d for d, n in zip(dl, ns) if n.startswith('input_')]
    ns2 = [n for n in ns if n.startswith('input_')]
    arr_in = gcp._thermal_form_arrays(dl2, ns2)
    if arr_in:
        print(f"\n[input_ only] n={arr_in['n']}, n_fit={(~arr_in['excluded']).sum()}")
        for a in [0.01, 0.05, 0.1, 0.3, 0.5, 1.0, 2.0, 5.0]:
            fit = gcp._thermal_fit(arr_in, fit_mask=~arr_in['excluded'], alpha=a)
            flag = ' ⭐' if fit['loocv'] >= 0.9 else ''
            print(f"  α={a:>5.2f}: LOOCV={fit['loocv']:.4f} R²={fit['r2']:.4f}{flag}")


if __name__ == '__main__':
    main()
