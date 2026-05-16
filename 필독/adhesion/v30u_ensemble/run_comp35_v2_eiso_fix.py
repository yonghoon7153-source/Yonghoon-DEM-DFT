"""run_comp35_v2_eiso_fix.py — proper eiso_fix for comp3_v2 and comp5_v2.
   Same protocol as run_comp4_v2_eiso_fix.py: NCM in each SE's own cell.
"""
import json, time
from pathlib import Path
import numpy as np
from ase.io import read

WORK = Path('/data/work/v30u_ensemble')
NCM  = WORK / 'ncm_5x5x1_PRESERVED.xyz'
SE_FILES = {
    'comp3_v2': WORK / 'comp3_slab_v2_PRESERVED.xyz',
    'comp5_v2': WORK / 'comp5_slab_v2_PRESERVED.xyz',
}
# Reference: comp4_v1 cell (the same NCM used → 그 cell 의 E_ncm 가 OLD reference)
SE_REF = WORK / 'comp4_slab_v1_PRESERVED.xyz'
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

    ncm = read(NCM)
    
    # Reference E_ncm (in comp4_v1 SE cell — same convention as comp1/2/4 eiso fix)
    se_ref = read(SE_REF)
    A_ref = xy_area(se_ref.cell.array)
    ncm_ref = ncm_in_se_cell(se_ref, ncm)
    ncm_ref.calc = calc
    E_ncm_ref = float(ncm_ref.get_potential_energy())
    print(f"REF: comp4_v1 SE cell  A={A_ref:.2f}  E_ncm_REF={E_ncm_ref:.4f} eV\n")

    # Each target comp
    for tag, se_path in SE_FILES.items():
        se = read(se_path)
        A_se = xy_area(se.cell.array)
        print(f"═══ {tag} ═══")
        print(f"  SE cell area: {A_se:.2f} Å² (mismatch vs REF: {A_se/A_ref:.4f})")

        ncm_se = ncm_in_se_cell(se, ncm)
        ncm_se.calc = calc
        E_ncm_NEW = float(ncm_se.get_potential_energy())
        print(f"  E_ncm in {tag} SE cell = {E_ncm_NEW:.4f} eV")

        dE = E_ncm_NEW - E_ncm_ref
        dW = dE / A_se * 16.0218
        print(f"  ΔE_ncm = {dE:+.4f} eV")
        print(f"  ΔW_strain = {dW:+.4f} J/m²")

        # Save eiso JSON in same format as comp4_v1
        eiso_key = tag.replace('_v2', '')  # comp3, comp5
        out_path = WORK / 'v30u_1L_correct_results_eiso_fix' / f'{eiso_key}_done.json'
        eiso_json = {
            'comps': tag,
            'ncm_file': str(NCM.name),
            'se_file': str(se_path.name),
            'E_ncm_iso_OLD_NCM_cell': E_ncm_ref,
            'E_ncm_iso_NEW_SE_cell':  E_ncm_NEW,
            'E_ncm_iso':              E_ncm_NEW,   # use NEW
            'delta_E_ncm_eV':         dE,
            'delta_Wad_J_per_m2':     dW,
            'area_SE_cell_A2':        A_se,
            'area_NCM_cell_A2':       A_ref,  # placeholder
            '_source': 'computed by run_comp35_v2_eiso_fix.py',
        }
        json.dump(eiso_json, open(out_path, 'w'), indent=2)
        print(f"  Saved: {out_path}\n")

    print("DONE — now re-run plot_killer_v2_figure_n5.py")


if __name__ == "__main__":
    main()
