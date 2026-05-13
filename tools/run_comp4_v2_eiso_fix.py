"""run_comp4_v2_eiso_fix.py — proper eiso_fix for comp4_v2 (its own SE cell).

face-flip currently uses comp4_v1's ΔW_strain as proxy for comp4_v2. This is
inaccurate because comp4_v1 and comp4_v2 have different SE cells (different
anneal state). Proper fix: compute E_ncm in comp4_v2 SE cell.

Output:
  /data/work/v30u_ensemble/comp4_v2_eiso_fix.json
    {E_ncm_iso_v1_cell, E_ncm_iso_v2_cell, delta_E_ncm,
     A_se_v1, A_se_v2, delta_Wad_strain_v2}

Use this delta_Wad_strain_v2 in face-flip α-correction instead of v1's.
"""
import json, time
from pathlib import Path
import numpy as np
from ase.io import read

WORK = Path('/data/work/v30u_ensemble')
SE_V1 = WORK / 'comp4_slab_v1_PRESERVED.xyz'
SE_V2 = WORK / 'comp4_slab_v2_PRESERVED.xyz'   # symlink to .bak_anomaly
NCM   = WORK / 'ncm_5x5x1_PRESERVED.xyz'
VACUUM_TOP = 30.0


def ncm_in_se_cell(se, ncm):
    a = ncm.copy()
    a.wrap()
    a.translate([0, 0, -a.positions[:, 2].min()])
    z_extent = a.positions[:, 2].max() - a.positions[:, 2].min()
    new_cell = se.cell.array.copy()
    new_cell[2] = [0, 0, z_extent + VACUUM_TOP]
    a.set_cell(new_cell, scale_atoms=False)
    a.set_pbc([True, True, True])
    return a


def xy_area(cell):
    a1 = cell[0]; a2 = cell[1]
    return float(np.linalg.norm(np.cross(np.append(a1[:2], 0), np.append(a2[:2], 0))))


def main():
    print("Loading UMA-s-1p1...")
    from fairchem.core import pretrained_mlip
    from fairchem.core.calculate.ase_calculator import FAIRChemCalculator
    pred = pretrained_mlip.get_predict_unit("uma-s-1p1", device="cuda")
    calc = FAIRChemCalculator(pred, task_name="omat")
    print("UMA loaded.\n")

    se_v1 = read(SE_V1)
    se_v2 = read(SE_V2)
    ncm   = read(NCM)

    A_v1 = xy_area(se_v1.cell.array)
    A_v2 = xy_area(se_v2.cell.array)
    print(f"comp4_v1 SE cell area = {A_v1:.2f} Å²")
    print(f"comp4_v2 SE cell area = {A_v2:.2f} Å²")
    print(f"  mismatch v2/v1 = {A_v2/A_v1:.4f}\n")

    # E_ncm in comp4_v1 cell (re-compute to verify)
    ncm_v1 = ncm_in_se_cell(se_v1, ncm)
    ncm_v1.calc = calc
    E_ncm_v1 = float(ncm_v1.get_potential_energy())
    print(f"E_ncm in comp4_v1 SE cell = {E_ncm_v1:.4f} eV")

    # E_ncm in comp4_v2 cell (the NEW value we need)
    ncm_v2 = ncm_in_se_cell(se_v2, ncm)
    ncm_v2.calc = calc
    E_ncm_v2 = float(ncm_v2.get_potential_energy())
    print(f"E_ncm in comp4_v2 SE cell = {E_ncm_v2:.4f} eV")

    dE = E_ncm_v2 - E_ncm_v1
    print(f"\nΔE_ncm (v2 - v1) = {dE:+.4f} eV")
    print(f"  = {dE / A_v2 * 16.0218:+.4f} J/m² when normalized by A_v2")

    # Read existing comp4 eiso_fix (v1's) for original ΔW_strain
    f_old = WORK / 'v30u_1L_correct_results_eiso_fix' / 'comp4_done.json'
    if f_old.exists():
        d = json.load(open(f_old))
        dW_v1 = d['delta_Wad_J_per_m2']
        E_ncm_v1_old = d['E_ncm_iso_NEW_SE_cell']
        print(f"\nFrom comp4_v1 eiso_fix JSON:")
        print(f"  ΔW_strain (v1) = {dW_v1:+.4f} J/m²")
        print(f"  E_ncm v1 (stored) = {E_ncm_v1_old:.4f} eV   (sanity check)")

    out = {
        'comp':          'comp4_v2',
        'A_se_v1_A2':    A_v1,
        'A_se_v2_A2':    A_v2,
        'E_ncm_v1_eV':   E_ncm_v1,
        'E_ncm_v2_eV':   E_ncm_v2,
        'dE_v2_minus_v1_eV':  dE,
        'dE_per_area_v2_Jm2': dE / A_v2 * 16.0218,
    }
    json.dump(out, open(WORK / 'comp4_v2_eiso_fix.json', 'w'), indent=2)
    print(f"\nSaved: {WORK / 'comp4_v2_eiso_fix.json'}")


if __name__ == "__main__":
    main()
