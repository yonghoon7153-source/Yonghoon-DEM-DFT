"""run_v30u_1L.py — Paper-protocol replica using 1L NCM PRESERVED.

Replaces the ncm_*_3Lconv.xyz with ncm_*_PRESERVED.xyz (1L conv, 3 atomic layers)
which matches the original paper protocol (phase1_rigid_binding.py).

Same SE slabs and 5z × 36xy ensemble as run_v30u_full_ensemble.py — only NCM
file path differs.

Output: v30u_1L_results/{comp}_done.json
"""
import os, json, time, numpy as np
from pathlib import Path
from ase.io import read
from fairchem.core import pretrained_mlip
from fairchem.core.calculate.ase_calculator import FAIRChemCalculator
import sys

sys.path.insert(0, '.')
from run_v30u_full_ensemble import (
    zshift_variant, stack_rigid, xy_area, log,
    N_ZSHIFTS, N_XY_GRID, GAP_MIN, GAP_MAX, GAP_STEP,
)
import numpy as np
gaps = np.arange(GAP_MIN, GAP_MAX + GAP_STEP/2, GAP_STEP)
xy_shifts = [(i/N_XY_GRID, j/N_XY_GRID)
             for i in range(N_XY_GRID) for j in range(N_XY_GRID)]


# Paper protocol: 1L NCM (PRESERVED), not 3Lconv
COMP_SPEC = {
    'comp1':  {'src': 'comp1_slab_v2.xyz',                  'ncm': 'ncm_7x7x1_PRESERVED.xyz'},
    'comp2':  {'src': 'comp2_slab_v2.xyz',                  'ncm': 'ncm_7x7x1_PRESERVED.xyz'},
    'comp3':  {'src': 'comp3_slab_v1_PRESERVED.xyz',        'ncm': 'ncm_5x5x1_PRESERVED.xyz'},
    'comp4':  {'src': 'comp4_slab_v1_PRESERVED.xyz',        'ncm': 'ncm_5x5x1_PRESERVED.xyz'},
    'comp5':  {'src': 'comp5_slab_v1_PRESERVED.xyz',        'ncm': 'ncm_5x5x1_PRESERVED.xyz'},
    'modelC': {'src': 'modelC_slab_v2_PRESERVED.xyz',       'ncm': 'ncm_5x5x1_PRESERVED.xyz'},
}

predictor = pretrained_mlip.get_predict_unit("uma-s-1p1", device="cuda")
calc = FAIRChemCalculator(predictor, task_name="omat")

WORK = Path('/data/work/v30u_ensemble')
RESULTS = WORK / 'v30u_1L_results'
RESULTS.mkdir(exist_ok=True)

t_start = time.time()
for c, spec in COMP_SPEC.items():
    checkpoint = RESULTS / f"{c}_done.json"
    if checkpoint.exists():
        log(f"[{c}] already done, skip")
        continue
    log(f"\n=== {c} (NCM={spec['ncm']}) ===")
    se_base = read(WORK / spec['src'])
    ncm = read(WORK / spec['ncm'])
    ncm.calc = calc
    E_ncm = float(ncm.get_potential_energy())
    log(f"  NCM={len(ncm)} atoms, E_ncm = {E_ncm:.3f} eV")

    E_se_per_z = []
    for iz in range(N_ZSHIFTS):
        se_z = zshift_variant(se_base, iz / N_ZSHIFTS)
        se_z.calc = calc
        E_se_per_z.append(float(se_z.get_potential_energy()))

    comp_data = {'gaps': gaps.tolist(),
                 'Wad_samples': {f"{g:.3f}": [] for g in gaps}}
    n_configs = N_ZSHIFTS * len(xy_shifts)
    idx = 0
    t1 = time.time()
    for iz in range(N_ZSHIFTS):
        se_z = zshift_variant(se_base, iz / N_ZSHIFTS)
        E_se = E_se_per_z[iz]
        for ixy, (dx, dy) in enumerate(xy_shifts):
            idx += 1
            for gap in gaps:
                stacked = stack_rigid(se_z, ncm, gap, shift_frac=(dx, dy))
                stacked.calc = calc
                E_int = float(stacked.get_potential_energy())
                A = xy_area(stacked.cell.array)
                wad = (E_se + E_ncm - E_int) / A * 16.0218
                comp_data['Wad_samples'][f"{gap:.3f}"].append(wad)
            if idx % 5 == 0 or idx == n_configs:
                el = time.time() - t1
                eta = el * (n_configs - idx) / idx
                log(f"  {c}: {idx}/{n_configs}  z{iz} xy{ixy}  "
                    f"el={el/60:.1f}min ETA={eta/60:.1f}min")

    comp_data['Wad_mean'] = []
    comp_data['Wad_std'] = []
    for g in gaps:
        s = comp_data['Wad_samples'][f"{g:.3f}"]
        comp_data['Wad_mean'].append(float(np.mean(s)))
        comp_data['Wad_std'].append(float(np.std(s)))
    comp_data['n_samples'] = n_configs
    comp_data['ncm_file'] = spec['ncm']

    json.dump(comp_data, open(checkpoint, 'w'), indent=2)
    log(f"  saved {checkpoint.name}")

log(f"\n=== TOTAL: {(time.time()-t_start)/3600:.2f} h ===")
