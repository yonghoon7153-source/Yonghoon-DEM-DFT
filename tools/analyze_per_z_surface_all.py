"""analyze_per_z_surface_all.py — per-z surface composition for all 4 comps.

For each comp (comp1, comp2, comp4_v1, modelC) and each of 5 z-shifts,
report:
  - Atoms within 2 Å of SE bottom face (NCM-facing)
  - Counts of Li, S, P, Cl, Br
  - Wad_well at that z (from existing eiso_fix JSON, 36-reg mean)
  - Wad_asymp at that z

Identifies for each comp the z with least Cl exposure ('canonical' termination).
Pure post-processing (~1 s), no new SCFs.

Run on gabia:
  cd /data/work/v30u_ensemble
  python3 analyze_per_z_surface_all.py
"""
import json
from pathlib import Path
import numpy as np
from ase.io import read

WORK    = Path('/data/work/v30u_ensemble')
RESULTS = WORK / 'v30u_1L_correct_results_eiso_fix'
OUT     = WORK / 'per_z_surface_summary.json'

COMPS = {
    'comp1':  'comp1_slab_v2.xyz',
    'comp2':  'comp2_slab_v2.xyz',
    'comp4':  'comp4_slab_v1_PRESERVED.xyz',
    'modelC': 'modelC_slab_v2_PRESERVED.xyz',
}

N_ZSHIFTS    = 5
SURFACE_DEPTH = 2.0   # Å from SE bottom face


def zshift_variant(atoms, frac):
    a = atoms.copy()
    cz = a.cell.lengths()[2]
    pos = a.positions.copy()
    pos[:, 2] = (pos[:, 2] + frac * cz) % cz
    a.set_positions(pos)
    return a


def surface_counts(se_zshifted):
    pos = se_zshifted.positions
    syms = se_zshifted.get_chemical_symbols()
    z_min = pos[:, 2].min()
    mask = pos[:, 2] <= (z_min + SURFACE_DEPTH)
    counts = {}
    for s, m in zip(syms, mask):
        if m:
            counts[s] = counts.get(s, 0) + 1
    counts['total'] = int(mask.sum())
    return counts


def main():
    summary = {}
    for c, xyz in COMPS.items():
        f_xyz = WORK / xyz
        f_json = RESULTS / f"{c}_done.json"
        if not f_xyz.exists():
            print(f"[SKIP] {c}: no xyz at {f_xyz}")
            continue
        if not f_json.exists():
            print(f"[SKIP] {c}: no eiso_fix JSON")
            continue
        se = read(f_xyz)
        d = json.load(open(f_json))

        # Per-z Wad mean over 36 reg (from eiso_fix data)
        per_z_wad_well = []
        per_z_wad_asymp = []
        gaps = d['gaps']
        for iz in range(N_ZSHIFTS):
            z_data = d['Wad_per_z_per_reg'].get(f"z{iz}", {})
            wad_per_gap = []
            for gk in [f"{g:.3f}" for g in gaps]:
                vals = [r['curve'][gk]['Wad_J_per_m2']
                        for r in z_data.values()
                        if r['curve'].get(gk, {}).get('Wad_J_per_m2') is not None]
                wad_per_gap.append(float(np.mean(vals)) if vals else np.nan)
            wad_arr = np.array(wad_per_gap)
            per_z_wad_well.append(float(np.nanmax(wad_arr)))
            per_z_wad_asymp.append(float(wad_arr[-1]))

        # Per-z surface composition
        print(f"\n══ {c} ══  (SE = {xyz})")
        print(f"  {'z':<3} {'total':>5} {'Li':>4} {'S':>4} {'P':>4} {'Cl':>4} {'Br':>4} "
              f"{'O':>4} {'Ni':>4} {'Co':>4} {'Mn':>4}  "
              f"{'Wad_well':>10} {'Wad_asymp':>10}")
        z_results = []
        for iz in range(N_ZSHIFTS):
            se_z = zshift_variant(se, iz / N_ZSHIFTS)
            cnt = surface_counts(se_z)
            row = (cnt.get('total', 0), cnt.get('Li', 0), cnt.get('S', 0),
                   cnt.get('P', 0), cnt.get('Cl', 0), cnt.get('Br', 0),
                   cnt.get('O', 0), cnt.get('Ni', 0), cnt.get('Co', 0),
                   cnt.get('Mn', 0))
            z_results.append({
                'iz': iz, 'counts': cnt,
                'Wad_well': per_z_wad_well[iz],
                'Wad_asymp': per_z_wad_asymp[iz],
            })
            wad_well = per_z_wad_well[iz]
            wad_asym = per_z_wad_asymp[iz]
            print(f"  z{iz:<2} {row[0]:>5d} {row[1]:>4d} {row[2]:>4d} {row[3]:>4d} "
                  f"{row[4]:>4d} {row[5]:>4d} {row[6]:>4d} {row[7]:>4d} {row[8]:>4d} "
                  f"{row[9]:>4d}  {wad_well:>+10.4f} {wad_asym:>+10.4f}")

        # Identify min-Cl z (and min-halogen z)
        z_by_cl = sorted(z_results, key=lambda r: r['counts'].get('Cl', 0))
        z_by_halogen = sorted(z_results,
                              key=lambda r: r['counts'].get('Cl', 0) + r['counts'].get('Br', 0))
        z_by_li = sorted(z_results, key=lambda r: -r['counts'].get('Li', 0))   # most Li
        print(f"  → min-Cl  z: z{z_by_cl[0]['iz']}     "
              f"(Cl_surf={z_by_cl[0]['counts'].get('Cl', 0)}, "
              f"Wad_well={z_by_cl[0]['Wad_well']:+.4f})")
        print(f"  → min-halogen z: z{z_by_halogen[0]['iz']}     "
              f"(Cl+Br={z_by_halogen[0]['counts'].get('Cl', 0) + z_by_halogen[0]['counts'].get('Br', 0)}, "
              f"Wad_well={z_by_halogen[0]['Wad_well']:+.4f})")
        print(f"  → max-Li z: z{z_by_li[0]['iz']}     "
              f"(Li_surf={z_by_li[0]['counts'].get('Li', 0)}, "
              f"Wad_well={z_by_li[0]['Wad_well']:+.4f})")

        summary[c] = {
            'xyz': xyz,
            'per_z': z_results,
            'min_Cl_z':       z_by_cl[0]['iz'],
            'min_halogen_z':  z_by_halogen[0]['iz'],
            'max_Li_z':       z_by_li[0]['iz'],
        }

    json.dump(summary, open(OUT, 'w'), indent=2)
    print(f"\nSaved: {OUT}")
    print("\nWhat to look for:")
    print("  • comp1/comp2 (Li6): do any z expose Cl/Br that we've been mixing in 5z mean?")
    print("    If yes → some z's are 'normal' Li6 surface; others are halogen-rich.")
    print("  • comp4 v1: how does it compare to the upcoming comp4_v2 z-screening?")
    print("  • modelC (Cl1.6): obvious Cl-rich surface in most z?")
    print("  • The 'canonical' z (max-Li or min-halogen) gives the cleanest cross-comp comparison.")


if __name__ == "__main__":
    main()
