"""Extract binding curves to CSV for Origin plotting.

Reads two JSON sources and outputs Origin-friendly CSVs:
  Source 1: phase2a_v28_figures/F1_data.json
            geometric Cl-O / Li-O / Br-O density vs gap (per comp)
  Source 2: phase2a_v30_results/summary.json
            MACE Wad (J/m²) vs gap (per comp)

Output format (per CSV):
  gap_A, comp1, comp2, comp3, comp4, comp5, modelC

Usage (run locally on downloaded paper2_data):
  cd /mnt/c/Users/안용훈/Downloads/paper2_data
  python3 extract_binding_curves_csv.py
  # → output/binding_*.csv
"""
import json
import os
from pathlib import Path

OUT_DIR = Path("binding_curves_csv"); OUT_DIR.mkdir(exist_ok=True)
ALL_COMPS = ['comp1', 'comp2', 'comp3', 'comp4', 'comp5', 'modelC']


def write_csv(filename, gaps, data_per_comp, x_label='gap_A'):
    path = OUT_DIR / filename
    with open(path, 'w', encoding='utf-8') as f:
        # header
        f.write(x_label + ',' + ','.join(ALL_COMPS) + '\n')
        # rows
        for i, gap in enumerate(gaps):
            row = [f"{gap:.3f}"]
            for c in ALL_COMPS:
                if c in data_per_comp and i < len(data_per_comp[c]):
                    v = data_per_comp[c][i]
                    row.append(f"{v:.6f}")
                else:
                    row.append("")
            f.write(','.join(row) + '\n')
    print(f"  wrote {path}  ({len(gaps)} rows × {len(ALL_COMPS)} comps)")


def extract_v28_geometric():
    """v28 F1_data.json → 3 CSVs (Cl-O, Li-O, Br-O)."""
    path = Path("phase2a_v28_figures/F1_data.json")
    if not path.exists():
        print(f"  SKIP: {path} not found")
        return
    print(f"\nReading {path}")
    d = json.load(open(path))
    # Get gap axis from any comp
    gaps = None
    for c in ALL_COMPS:
        if c in d:
            gaps = d[c]['gap']
            break
    if not gaps:
        print(f"  no gap axis found in {path}")
        return

    for bond in ['Cl-O', 'Li-O', 'Br-O']:
        per_comp = {c: d[c][bond] for c in ALL_COMPS if c in d}
        write_csv(f"binding_geometric_{bond.replace('-', '_')}_density.csv",
                   gaps, per_comp, x_label='gap_A')


def extract_v30_mace():
    """v30 summary.json → 1 CSV (Wad MACE)."""
    path = Path("phase2a_v30_results/summary.json")
    if not path.exists():
        print(f"  SKIP: {path} not found — sftp from KISTI:")
        print(f"    /scratch/x3430a02/kgy/manuscript_support/adhesion_v5_v2/phase2a_v30_results/")
        return
    print(f"\nReading {path}")
    d = json.load(open(path))
    # Find a sample wad_curve to extract gaps
    gaps = None
    for c in ALL_COMPS:
        if c in d and 'wad_curve' in d[c]:
            gaps = [pt['gap'] for pt in d[c]['wad_curve']]
            break
    if not gaps:
        print(f"  no wad_curve found in {path}")
        return

    per_comp_wad = {}
    per_comp_eint = {}
    for c in ALL_COMPS:
        if c in d and 'wad_curve' in d[c]:
            per_comp_wad[c] = [pt['Wad'] for pt in d[c]['wad_curve']]
            per_comp_eint[c] = [pt['E_int'] for pt in d[c]['wad_curve']]

    write_csv("binding_MACE_Wad_J_m2.csv", gaps, per_comp_wad, x_label='gap_A')
    write_csv("binding_MACE_Eint_eV.csv", gaps, per_comp_eint, x_label='gap_A')


def write_summary_table():
    """Per-comp equilibrium summary."""
    GAP_EQ = {'comp1': 1.2, 'comp2': 1.2, 'comp3': 1.4, 'comp4': 1.6, 'comp5': 1.6, 'modelC': 1.2}
    PAPER_EXP = {'comp1': 194, 'comp2': 180, 'comp3': 316, 'comp4': 298, 'comp5': 249, 'modelC': None}
    FAMILY = {'comp1': 'Li6', 'comp2': 'Li6', 'comp3': 'Li5.4', 'comp4': 'Li5.4',
              'comp5': 'Li5.4', 'modelC': 'Li5.4'}

    # Pull v15 Cl-O density at gap_eq (or best from F1)
    f1 = Path("phase2a_v28_figures/F1_data.json")
    cl_o_eq = {}
    li_o_eq = {}
    br_o_eq = {}
    if f1.exists():
        d = json.load(open(f1))
        for c in ALL_COMPS:
            if c not in d:
                continue
            gaps = d[c]['gap']
            i_eq = min(range(len(gaps)), key=lambda i: abs(gaps[i] - GAP_EQ[c]))
            cl_o_eq[c] = d[c]['Cl-O'][i_eq]
            li_o_eq[c] = d[c]['Li-O'][i_eq]
            br_o_eq[c] = d[c]['Br-O'][i_eq]

    # Pull v30 W_max + d_min
    v30 = Path("phase2a_v30_results/summary.json")
    w_max = {}
    d_min = {}
    if v30.exists():
        s = json.load(open(v30))
        for c in ALL_COMPS:
            if c in s:
                w_max[c] = s[c].get('W_max_J_per_m2')
                d_min[c] = s[c].get('d_min_A')

    out = OUT_DIR / "summary_per_comp.csv"
    def fmt(v, fmt_spec):
        return format(v, fmt_spec) if v is not None else ''
    with open(out, 'w', encoding='utf-8') as f:
        f.write("comp,family,gap_eq_A,paper_exp_Wad_mJ_m2,Cl-O_density_eq,Li-O_density_eq,"
                "Br-O_density_eq,MACE_W_max_J_m2,MACE_d_min_A\n")
        for c in ALL_COMPS:
            f.write(f"{c},{FAMILY[c]},{GAP_EQ[c]:.1f},"
                    f"{PAPER_EXP[c] if PAPER_EXP[c] is not None else ''},"
                    f"{fmt(cl_o_eq.get(c), '.6f')},"
                    f"{fmt(li_o_eq.get(c), '.6f')},"
                    f"{fmt(br_o_eq.get(c), '.6f')},"
                    f"{fmt(w_max.get(c), '.4f')},"
                    f"{fmt(d_min.get(c), '.2f')}\n")
    print(f"  wrote {out}")


def main():
    print("=" * 60)
    print("Extracting binding curves for Origin plotting")
    print("=" * 60)
    extract_v28_geometric()
    extract_v30_mace()
    write_summary_table()
    print(f"\nAll CSVs in: {OUT_DIR.resolve()}")
    print("\nOrigin import: drag .csv into Origin worksheet, set first col as X.")


if __name__ == "__main__":
    main()
