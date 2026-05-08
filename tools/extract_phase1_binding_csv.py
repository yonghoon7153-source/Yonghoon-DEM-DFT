"""Convert Phase 1 binding_curves.json (UMA) to Origin-friendly CSVs.

Phase 1 saved 36 xy-shift registries × ~20 gap points per comp. Output:
  - binding_UMA_Wad_mean.csv: gap vs mean(Wad) over 36 registries
  - binding_UMA_Wad_std.csv:  gap vs std(Wad) over 36 registries
  - binding_UMA_Wad_max.csv:  gap vs max(Wad) per gap (i.e., best registry)
  - binding_UMA_Wad_R1origin.csv: gap vs Wad at R1_origin only (single registry)
  - binding_UMA_Eint_mean.csv: gap vs mean(E_int) eV over registries

All in J/m² (Wad) or eV (E_int).

Usage:
  cd /mnt/c/Users/안용훈/Downloads/paper2_data
  python3 extract_phase1_binding_csv.py
  # → output/binding_UMA_*.csv
"""
import json
from pathlib import Path
import statistics

OUT_DIR = Path("binding_curves_csv"); OUT_DIR.mkdir(exist_ok=True)
ALL_COMPS = ['comp1', 'comp2', 'comp3', 'comp4', 'comp5', 'modelC']
PATH_BIND = Path("phase1_results/binding_curves.json")


def collect_gap_axis(d):
    """Collect union of all gap strings used across registries."""
    gap_set = set()
    for comp in ALL_COMPS:
        if comp not in d:
            continue
        for reg, reg_data in d[comp].items():
            for gap_str in reg_data.get('curve', {}):
                gap_set.add(gap_str)
    return sorted(gap_set, key=float)


def stat_at_gap(d, comp, gap_str, key='Wad_J_per_m2'):
    """List of values at given (comp, gap) across all registries."""
    if comp not in d:
        return []
    vals = []
    for reg, reg_data in d[comp].items():
        curve = reg_data.get('curve', {})
        if gap_str in curve and key in curve[gap_str]:
            vals.append(curve[gap_str][key])
    return vals


def write_csv(name, gaps, per_comp, header_xlabel='gap_A'):
    out = OUT_DIR / name
    with open(out, 'w', encoding='utf-8') as f:
        f.write(header_xlabel + ',' + ','.join(ALL_COMPS) + '\n')
        for gap_str in gaps:
            row = [gap_str]
            for c in ALL_COMPS:
                v = per_comp.get(c, {}).get(gap_str)
                if v is None:
                    row.append('')
                else:
                    row.append(f"{v:.6f}")
            f.write(','.join(row) + '\n')
    print(f"  wrote {out}")


def main():
    if not PATH_BIND.exists():
        print(f"ERROR: {PATH_BIND} not found.")
        print("Make sure you've sftp'd the phase1_results dir from KISTI:")
        print("  sftp> get -r /scratch/x3430a02/kgy/manuscript_support/adhesion_v5_v2/phase1_results")
        return
    d = json.load(open(PATH_BIND))
    gaps = collect_gap_axis(d)
    print(f"Found {len(gaps)} gap points: {gaps[0]} - {gaps[-1]} A")

    # mean / std / max / R1_origin / E_int_mean
    mean_wad = {c: {} for c in ALL_COMPS}
    std_wad  = {c: {} for c in ALL_COMPS}
    max_wad  = {c: {} for c in ALL_COMPS}
    r1_wad   = {c: {} for c in ALL_COMPS}
    mean_eint = {c: {} for c in ALL_COMPS}

    for c in ALL_COMPS:
        if c not in d:
            print(f"  WARN: {c} not in binding_curves.json")
            continue
        for gap_str in gaps:
            vals_wad = stat_at_gap(d, c, gap_str, 'Wad_J_per_m2')
            vals_e   = stat_at_gap(d, c, gap_str, 'E_int')
            if vals_wad:
                mean_wad[c][gap_str] = sum(vals_wad)/len(vals_wad)
                std_wad[c][gap_str]  = statistics.stdev(vals_wad) if len(vals_wad) > 1 else 0.0
                max_wad[c][gap_str]  = max(vals_wad)
            if vals_e:
                mean_eint[c][gap_str] = sum(vals_e)/len(vals_e)
            r1 = d[c].get('R1_origin', {}).get('curve', {}).get(gap_str, {})
            if 'Wad_J_per_m2' in r1:
                r1_wad[c][gap_str] = r1['Wad_J_per_m2']

    write_csv("binding_UMA_Wad_mean_J_m2.csv", gaps, mean_wad)
    write_csv("binding_UMA_Wad_std_J_m2.csv",  gaps, std_wad)
    write_csv("binding_UMA_Wad_max_J_m2.csv",  gaps, max_wad)
    write_csv("binding_UMA_Wad_R1origin_J_m2.csv", gaps, r1_wad)
    write_csv("binding_UMA_Eint_mean_eV.csv",  gaps, mean_eint)

    # Per-comp summary: Wad max + d at max
    print("\n--- Per-comp W_max + d_min (UMA Phase 1) ---")
    print(f"{'comp':<8} {'W_max(J/m²)':>13} {'d_min(A)':>10}  {'mean@d_min':>12} {'std@d_min':>10}")
    for c in ALL_COMPS:
        if not max_wad[c]:
            continue
        best_gap = max(max_wad[c].keys(), key=lambda g: max_wad[c][g])
        wm = max_wad[c][best_gap]
        # mean at same gap
        m = mean_wad[c].get(best_gap, 0)
        s = std_wad[c].get(best_gap, 0)
        print(f"  {c:<8} {wm:>+13.4f} {best_gap:>10}  {m:>+12.4f} {s:>10.4f}")

    print(f"\nAll CSVs in: {OUT_DIR.resolve()}")
    print("\nOrigin import: drag CSV into worksheet, set first column as X.")
    print("\nRecommended for paper figure (binding curve):")
    print("  binding_UMA_Wad_mean_J_m2.csv  +  binding_UMA_Wad_std_J_m2.csv")
    print("  → plot mean as line, std as error band per comp")


if __name__ == "__main__":
    main()
