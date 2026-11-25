#!/usr/bin/env python
"""Face-flip Wad_well sweep for comp4_v2 across z-shifts 0,1,3,4.
shift 2 already exists in face_flip_results/comp4_v2_done.json — skip.

For each shift: face A + face B, mean over 36 registries x 16 gaps.
Output: comp4_v2_shift{N}_facflip.json  +  summary printout.

Run from /data/work/v30u_ensemble/
"""
import json, time, os, sys
from pathlib import Path
import numpy as np
import ase.io
from ase.calculators.singlepoint import SinglePointCalculator

# Re-use main face_flip routine from existing script
sys.path.insert(0, '/data/work/v30u_ensemble')
from run_v30u_1L_face_flip import run_face_flip_one_comp, load_uma, COMPS

WORK = Path('/data/work/v30u_ensemble')
OUT  = WORK / 'face_flip_results'
SLAB_TEMPLATE = WORK / 'comp4_v2_slab_shift{n}.xyz'

SHIFTS_TO_RUN = [0, 1, 3, 4]   # shift 2 already done

def main():
    t0 = time.time()
    calc = load_uma()
    print(f"[{time.strftime('%H:%M:%S')}] UMA loaded.")

    results = {}
    for s in SHIFTS_TO_RUN:
        slab_file = SLAB_TEMPLATE.format(n=s)
        if not Path(slab_file).exists():
            print(f"  MISSING: {slab_file} — skip shift {s}")
            continue
        print(f"\n========= comp4_v2  shift {s}  ({slab_file}) =========")
        # Override the slab path inside COMPS dict
        original = COMPS['comp4_v2']['slab']
        COMPS['comp4_v2']['slab'] = str(slab_file)
        try:
            res = run_face_flip_one_comp('comp4_v2', calc)
            out_json = OUT / f'comp4_v2_shift{s}_done.json'
            json.dump(res, open(out_json, 'w'), indent=2, default=str)
            results[s] = {
                'A_well': res['faces']['A']['Wad_well_mean'],
                'A_asymp': res['faces']['A']['Wad_asymp_mean'],
                'B_well': res['faces']['B']['Wad_well_mean'],
                'B_asymp': res['faces']['B']['Wad_asymp_mean'],
            }
            print(f"  shift {s}: A well={results[s]['A_well']:+.4f}  B well={results[s]['B_well']:+.4f}")
        finally:
            COMPS['comp4_v2']['slab'] = original

    print("\n" + "=" * 70)
    print("Summary  comp4_v2 across shifts:")
    print(f"{'shift':>5}  {'A_well':>8}  {'A_asymp':>8}  {'B_well':>8}  {'B_asymp':>8}")
    for s in sorted(results):
        r = results[s]
        print(f"{s:>5}  {r['A_well']:+8.4f}  {r['A_asymp']:+8.4f}  {r['B_well']:+8.4f}  {r['B_asymp']:+8.4f}")

    # Existing shift 2 for comparison
    sh2 = json.load(open(OUT / 'comp4_v2_done.json'))
    print(f"{'2*':>5}  {sh2['faces']['A']['Wad_well_mean']:+8.4f}  {sh2['faces']['A']['Wad_asymp_mean']:+8.4f}  "
          f"{sh2['faces']['B']['Wad_well_mean']:+8.4f}  {sh2['faces']['B']['Wad_asymp_mean']:+8.4f}   (existing)")

    print(f"\nTotal time: {(time.time()-t0)/60:.1f} min")

if __name__ == '__main__':
    main()
