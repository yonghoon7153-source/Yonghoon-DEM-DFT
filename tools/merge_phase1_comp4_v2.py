"""Merge comp4 v2 phase1 result into existing binding_curves.json.

After running phase1_comp4_v2_only.py on KISTI, transfer
phase1_comp4_v2_only_results/binding_curves.json to local
paper2_data/, then run this to merge into the master binding_curves.json
and rerun the plot.

Usage (on Windows WSL paper2_data):
    python3 tools/merge_phase1_comp4_v2.py \\
        --orig phase1_results/binding_curves.json \\
        --comp4 phase1_comp4_v2_only_results/binding_curves.json \\
        --out  phase1_v2_results/binding_curves.json

Then:
    cp phase1_v2_results/binding_curves.json phase1_results/  # or symlink
    python3 extract_phase1_binding_csv.py
    python3 plot_binding_curves.py
    # → updated binding_curves_main.png with comp4 v2

Outputs:
    Merged binding_curves.json with comp4 entry replaced by v2 result.
    All other comps (comp1/2/3/5/modelC) unchanged.
"""
import argparse
import json
from pathlib import Path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--orig', required=True,
                    help='Original phase1_results/binding_curves.json')
    ap.add_argument('--comp4', required=True,
                    help='New comp4 v2 phase1 binding_curves.json (key may be "comp4_v2" or "comp4")')
    ap.add_argument('--out', required=True, help='Output merged JSON')
    args = ap.parse_args()

    orig = json.load(open(args.orig))
    new = json.load(open(args.comp4))

    # New JSON might have key "comp4_v2" or "comp4" — handle both
    if 'comp4_v2' in new:
        comp4_data = new['comp4_v2']
    elif 'comp4' in new:
        comp4_data = new['comp4']
    else:
        raise SystemExit(f"new file has no 'comp4' or 'comp4_v2' key. Keys: {list(new.keys())}")

    # Sanity check: must have R1_origin etc
    if 'R1_origin' not in comp4_data:
        raise SystemExit(f"new comp4 data missing R1_origin. Keys: {list(comp4_data.keys())[:5]}")

    n_reg_orig = len(orig['comp4'])
    n_reg_new = len(comp4_data)
    print(f"Original comp4 registries: {n_reg_orig}")
    print(f"New comp4 v2 registries:   {n_reg_new}")
    if n_reg_new < n_reg_orig:
        print(f"  WARN: new has fewer registries — partial merge")

    # Replace comp4 in orig
    orig['comp4'] = comp4_data
    print(f"\nReplaced 'comp4' entry. Merged JSON has {len(orig)} comps:")
    for c in orig:
        print(f"  {c}: {len(orig[c])} registries")

    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    json.dump(orig, open(args.out, 'w'), indent=2)
    print(f"\nSaved: {args.out}")
    print(f"\nNext: replace phase1_results/binding_curves.json with this and rerun plot_binding_curves.py")


if __name__ == '__main__':
    main()
