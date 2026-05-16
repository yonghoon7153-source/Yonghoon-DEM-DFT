"""normalize_wad_by_surface_Li.py — test Li-density hypothesis on eiso-fixed data.

Question: is the Wad(Li6) > Wad(Li5.4) ordering simply because Li6 has more Li
atoms (6 vs 5.4 per formula unit) → more Li-O interface contacts in rigid scan?

If yes: normalizing Wad by surface-Li count should remove the family inversion
       and reveal paper-matching intrinsic chemistry.
If no:  the Li6 > Li5.4 ranking persists even per-Li → it's a real UMA prediction
       of stronger per-bond chemistry, not just density.

Method:
  1. Read each SE xyz → count Li atoms in the bottom layer (z within 3 Å of z_min,
     i.e. the face that meets NCM in stack_interface).
  2. Also count "interface-active" atoms = Li + Cl + Br + S in that layer (all
     potential contact partners for NCM oxygen).
  3. Read v30u_1L_correct_results_eiso_fix/{comp}_done.json → Wad_mean (5z×36).
  4. Compute:
       Wad_per_Li_fu      = Wad / (Li_per_fu)              ← per Li in formula unit
       Wad_per_surf_Li    = Wad × A / N_surf_Li            ← per surface Li atom
       Wad_per_surf_iface = Wad × A / N_surf_interface     ← per surface interface atom
  5. Compute R against paper_aJ for each metric, side by side.

Output: /data/work/v30u_ensemble/normalize_wad_summary.{json,csv}
        + stdout table.

Run on gabia:
  cd /data/work/v30u_ensemble
  python3 normalize_wad_by_surface_Li.py
"""
import json
from pathlib import Path
import numpy as np
from ase.io import read

WORK = Path('/data/work/v30u_ensemble')
RESULTS = WORK / 'v30u_1L_correct_results_eiso_fix'
OUT_JSON = WORK / 'normalize_wad_summary.json'
OUT_CSV  = WORK / 'normalize_wad_summary.csv'

COMPS = {
    'comp1':  {'se': 'comp1_slab_v2.xyz',            'Li_per_fu': 6.0},
    'comp2':  {'se': 'comp2_slab_v2.xyz',            'Li_per_fu': 6.0},
    'comp4':  {'se': 'comp4_slab_v1_PRESERVED.xyz',  'Li_per_fu': 5.4},
    'modelC': {'se': 'modelC_slab_v2_PRESERVED.xyz', 'Li_per_fu': 5.4},
}

PAPER_EXP = {'comp1': 194, 'comp2': 180, 'comp4': 298}   # aJ, modelC not in paper

SURFACE_DEPTH = 3.0    # Å from SE bottom face toward bulk
INTERFACE_ATOMS = {'Li', 'Cl', 'Br', 'S'}


def xy_area(cell):
    a1 = cell[0]; a2 = cell[1]
    cross = np.cross(a1[:2].tolist() + [0], a2[:2].tolist() + [0])
    return float(np.linalg.norm(cross))


def surface_counts(se):
    """Atoms within `SURFACE_DEPTH` Å of the SE face that meets NCM.

    In stack_interface, SE is translated so its z_min sits above NCM. So the
    'NCM-facing' SE atoms are those near z_min. We count them in the lab frame
    of the original SE xyz (no z-shift applied here).
    """
    pos = se.get_positions()
    syms = se.get_chemical_symbols()
    z_min = pos[:, 2].min()
    mask = pos[:, 2] <= (z_min + SURFACE_DEPTH)
    counts = {'Li': 0, 'P': 0, 'S': 0, 'Cl': 0, 'Br': 0, 'O': 0, 'Ni': 0, 'Co': 0, 'Mn': 0}
    for s, m in zip(syms, mask):
        if m:
            counts[s] = counts.get(s, 0) + 1
    counts['N_iface_atoms'] = sum(counts.get(s, 0) for s in INTERFACE_ATOMS)
    counts['N_surf_total']  = int(mask.sum())
    return counts


def pearson(x, y):
    x, y = np.asarray(x, dtype=float), np.asarray(y, dtype=float)
    if len(x) < 2:
        return None
    return float(np.corrcoef(x, y)[0, 1])


def main():
    rows = []
    for c, info in COMPS.items():
        f_json = RESULTS / f"{c}_done.json"
        f_xyz  = WORK / info['se']
        if not f_json.exists():
            print(f"  [SKIP] {c}: no JSON"); continue
        if not f_xyz.exists():
            print(f"  [SKIP] {c}: no xyz");  continue
        d = json.load(open(f_json))
        se = read(f_xyz)
        A_se = xy_area(se.cell.array)

        # Wad metrics (eiso-fix corrected)
        wad_mean = np.array(d['Wad_mean'], dtype=float)
        gaps     = np.array(d['gaps'],     dtype=float)
        i_well   = int(np.nanargmax(wad_mean))
        wad_well = float(wad_mean[i_well])
        d_well   = float(gaps[i_well])
        wad_asym = float(wad_mean[-1])

        # Surface composition
        cnt = surface_counts(se)
        N_Li     = max(cnt['Li'], 1)
        N_iface  = max(cnt['N_iface_atoms'], 1)

        # Normalizations
        wad_per_Li_fu       = wad_well / info['Li_per_fu']
        wad_per_surf_Li     = wad_well * A_se / N_Li          # J/m² × Å² / atom
        wad_per_surf_iface  = wad_well * A_se / N_iface

        rows.append({
            'comp':              c,
            'Li_per_fu':         info['Li_per_fu'],
            'A_se_A2':           A_se,
            'd_well_A':          d_well,
            'wad_well':          wad_well,
            'wad_asym':          wad_asym,
            'surf_Li_count':     cnt['Li'],
            'surf_P':            cnt['P'],
            'surf_S':            cnt['S'],
            'surf_Cl':           cnt['Cl'],
            'surf_Br':           cnt['Br'],
            'N_iface_atoms':     N_iface,
            'wad_per_Li_fu':       wad_per_Li_fu,
            'wad_per_surf_Li':     wad_per_surf_Li,
            'wad_per_surf_iface':  wad_per_surf_iface,
            'paper_aJ':          PAPER_EXP.get(c, None),
        })

    # ─── Table print ────────────────────────────────────────────
    print("\n" + "=" * 100)
    print(f"{'comp':<8} {'Li/fu':>6} {'A(Å²)':>7} {'surf_Li':>8} {'Wad':>7} "
          f"{'/Li_fu':>8} {'/surf_Li':>10} {'/iface':>9} {'paper_aJ':>9}")
    print("-" * 100)
    for r in rows:
        print(f"{r['comp']:<8} {r['Li_per_fu']:>6.1f} {r['A_se_A2']:>7.1f} "
              f"{r['surf_Li_count']:>8d} {r['wad_well']:>+7.3f} "
              f"{r['wad_per_Li_fu']:>+8.3f} {r['wad_per_surf_Li']:>+10.3f} "
              f"{r['wad_per_surf_iface']:>+9.3f} "
              f"{r['paper_aJ'] if r['paper_aJ'] is not None else '—':>9}")
    print("=" * 100)

    # ─── R metrics ──────────────────────────────────────────────
    paper_rows = [r for r in rows if r['paper_aJ'] is not None]
    if len(paper_rows) >= 2:
        pap = [r['paper_aJ'] for r in paper_rows]
        names = [r['comp']    for r in paper_rows]
        print(f"\n── Pearson R against paper aJ (n={len(pap)}: {names}) ──")
        for key, label in [
            ('wad_well',           'raw Wad_well            '),
            ('wad_per_Li_fu',      'Wad / Li_per_fu         '),
            ('wad_per_surf_Li',    'Wad × A / surf_Li_count '),
            ('wad_per_surf_iface', 'Wad × A / surf_iface    '),
        ]:
            metric = [r[key] for r in paper_rows]
            R = pearson(pap, metric)
            print(f"  {label}  →  R = {R:+.3f}  values={[f'{v:+.3f}' for v in metric]}")

    # ─── save ───────────────────────────────────────────────────
    json.dump({'rows': rows}, open(OUT_JSON, 'w'), indent=2)
    with open(OUT_CSV, 'w') as f:
        keys = ['comp', 'Li_per_fu', 'A_se_A2', 'surf_Li_count', 'N_iface_atoms',
                'wad_well', 'wad_per_Li_fu', 'wad_per_surf_Li',
                'wad_per_surf_iface', 'paper_aJ']
        f.write(",".join(keys) + "\n")
        for r in rows:
            f.write(",".join(str(r.get(k, '')) for k in keys) + "\n")
    print(f"\nSaved: {OUT_JSON}")
    print(f"Saved: {OUT_CSV}")
    print("\nInterpretation:")
    print("  • If R(per_surf_Li, paper) > R(raw, paper) → Li-density alone")
    print("    explains a chunk of the rigid Wad inversion.")
    print("  • If R(per_surf_Li, paper) still negative → density not the dominant")
    print("    factor; intrinsic per-bond chemistry favors Li6 in rigid scan.")
    print("    → Relax test needed (next step).")


if __name__ == "__main__":
    main()
