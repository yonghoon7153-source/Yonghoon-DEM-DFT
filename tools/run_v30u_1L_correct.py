"""run_v30u_1L_correct.py — Phase1-faithful 1L NCM ensemble with 5 z-shifts.

CRITICAL: Uses phase1_rigid_binding.py's stack_interface() VERBATIM
(scale_atoms=False, E_iso with vacuum, SE-cell-based combined).

Adds 5 z-shifts on top of phase1's 36-registry (6 sym + 30 random seed=42)
xy-shift scheme. Total per comp: 5 × 36 × n_gaps = 5 × 36 × 16 = 2880 SCF.

Run on: gabia
Comps: comp1, comp2, comp4, modelC (rerun after stack_rigid bug fix)
NCM: 1L PRESERVED convention (paper protocol)

Output: v30u_1L_correct_results/{comp}_done.json
"""
import os, json, time, gc
from pathlib import Path
import numpy as np
from ase.io import read

# CONFIG — only 4 comps user requested
COMPS = {
    'comp1':  {'se': 'comp1_slab_v2.xyz',            'ncm': 'ncm_7x7x1_PRESERVED.xyz'},
    'comp2':  {'se': 'comp2_slab_v2.xyz',            'ncm': 'ncm_7x7x1_PRESERVED.xyz'},
    'comp4':  {'se': 'comp4_slab_v1_PRESERVED.xyz',  'ncm': 'ncm_5x5x1_PRESERVED.xyz'},
    'modelC': {'se': 'modelC_slab_v2_PRESERVED.xyz', 'ncm': 'ncm_5x5x1_PRESERVED.xyz'},
}

# Phase1 D_VALUES (16 gaps)
D_VALUES = [0.6, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0, 2.2, 2.5, 2.8, 3.0, 3.5, 4.0, 5.0, 7.0]

# Phase1 registries (6 high-sym + 30 random, seed=42)
HIGH_SYM = [
    ("R1_origin",   (0.0, 0.0)),
    ("R2_half_x",   (0.5, 0.0)),
    ("R3_half_y",   (0.0, 0.5)),
    ("R4_diagonal", (0.5, 0.5)),
    ("R5_hex1",     (1/3, 2/3)),
    ("R6_hex2",     (2/3, 1/3)),
]
N_RANDOM = 30
RANDOM_SEED = 42
VACUUM_TOP = 30.0
N_ZSHIFTS = 5   # our addition: 5 z-shifts per comp

WORK = Path('/data/work/v30u_ensemble')
RESULTS = WORK / 'v30u_1L_correct_results'
RESULTS.mkdir(exist_ok=True)
LOG_FILE = RESULTS / 'progress.log'


def log(msg):
    s = f"[{time.strftime('%H:%M:%S')}] {msg}"
    print(s, flush=True)
    with open(LOG_FILE, 'a') as f:
        f.write(s + "\n")


# ========================================================================
#  PHASE1 FUNCTIONS — VERBATIM COPY from phase1_rigid_binding.py
# ========================================================================

def add_vacuum(atoms, vac):
    cell = atoms.cell.array.copy()
    cell[2, 2] += vac
    atoms.set_cell(cell, scale_atoms=False)
    atoms.set_pbc([True, True, True])
    return atoms


def stack_interface(se, ncm, gap, shift_frac):
    se_a = se.copy()
    ncm_a = ncm.copy()
    dx, dy = shift_frac
    shift_cart = dx * ncm_a.cell.array[0] + dy * ncm_a.cell.array[1]
    ncm_a.translate([shift_cart[0], shift_cart[1], 0])
    ncm_a.wrap()
    ncm_a.translate([0, 0, -ncm_a.positions[:, 2].min()])
    ncm_z_max = ncm_a.positions[:, 2].max()
    se_z_min = se_a.positions[:, 2].min()
    se_a.translate([0, 0, ncm_z_max - se_z_min + gap])
    combined = ncm_a + se_a
    new_cell = se.cell.array.copy()
    z_extent = combined.positions[:, 2].max() - combined.positions[:, 2].min()
    new_cell[2] = [0, 0, z_extent + VACUUM_TOP]
    combined.set_cell(new_cell, scale_atoms=False)
    combined.set_pbc([True, True, True])
    return combined


def xy_area(cell):
    a1 = cell[0]; a2 = cell[1]
    cross = np.cross(a1[:2].tolist() + [0], a2[:2].tolist() + [0])
    return np.linalg.norm(cross)


# ========================================================================
#  OUR ADDITION: z-shift variant
# ========================================================================

def zshift_variant(atoms, frac):
    """Shift SE atoms by frac × cell_c in z direction, wrap PBC."""
    a = atoms.copy()
    cz = a.cell.lengths()[2]
    pos = a.positions.copy()
    pos[:, 2] = (pos[:, 2] + frac * cz) % cz
    a.set_positions(pos)
    return a


# ========================================================================
#  CALC INIT (lazy)
# ========================================================================

_predictor = None


def make_calc():
    global _predictor
    from fairchem.core import pretrained_mlip
    from fairchem.core.calculate.ase_calculator import FAIRChemCalculator
    if _predictor is None:
        _predictor = pretrained_mlip.get_predict_unit("uma-s-1p1", device="cuda")
    return FAIRChemCalculator(_predictor, task_name="omat")


# ========================================================================
#  MAIN
# ========================================================================

def main():
    rng = np.random.default_rng(RANDOM_SEED)
    RANDOM_REG = [(f"rand_{i+1:03d}", (rng.uniform(0, 1), rng.uniform(0, 1)))
                  for i in range(N_RANDOM)]
    ALL_REG = HIGH_SYM + RANDOM_REG

    log("=" * 70)
    log(f"v30u_1L_correct ensemble — phase1-faithful stack + {N_ZSHIFTS} z-shifts")
    log(f"Comps: {list(COMPS.keys())}")
    log(f"Registries: {len(HIGH_SYM)} sym + {N_RANDOM} random = {len(ALL_REG)}")
    log(f"D_VALUES: {len(D_VALUES)} gaps  |  N_ZSHIFTS: {N_ZSHIFTS}")
    log(f"Total per comp: {N_ZSHIFTS * len(ALL_REG) * len(D_VALUES)} SCFs")
    log("=" * 70)

    log("\nLoading UMA-s-1p1...")
    calc = make_calc()
    log("UMA loaded.")

    t_start = time.time()

    for c, paths in COMPS.items():
        checkpoint = RESULTS / f"{c}_done.json"
        if checkpoint.exists():
            log(f"\n[{c}] checkpoint exists, skip")
            continue

        log(f"\n========= {c} (NCM={paths['ncm']}) =========")
        se_base = read(WORK / paths['se'])
        ncm = read(WORK / paths['ncm'])
        log(f"  SE: {len(se_base)} atoms  |  NCM: {len(ncm)} atoms")

        # E_iso for NCM (vacuum-added, like phase1)
        ncm_vac = add_vacuum(ncm.copy(), VACUUM_TOP)
        ncm_vac.calc = calc
        E_ncm = float(ncm_vac.get_potential_energy())
        log(f"  E_ncm (+vacuum) = {E_ncm:.4f} eV")

        # Per-z E_iso for SE (vacuum-added, per zshift_variant)
        E_se_per_z = []
        for iz in range(N_ZSHIFTS):
            se_z = zshift_variant(se_base, iz / N_ZSHIFTS)
            se_z_vac = add_vacuum(se_z, VACUUM_TOP)
            se_z_vac.calc = calc
            E_se_z = float(se_z_vac.get_potential_energy())
            E_se_per_z.append(E_se_z)
            log(f"  E_se z{iz} (+vacuum) = {E_se_z:.4f} eV")

        # Binding curves
        comp_data = {
            'comps': c,
            'ncm_file': paths['ncm'],
            'se_file': paths['se'],
            'gaps': D_VALUES,
            'registries': [r[0] for r in ALL_REG],
            'n_zshifts': N_ZSHIFTS,
            'E_ncm_iso': E_ncm,
            'E_se_iso_per_z': E_se_per_z,
            # Per-config results: per-z per-registry per-gap Wad
            'Wad_per_z_per_reg': {f"z{iz}": {} for iz in range(N_ZSHIFTS)},
            # Aggregated: mean over (z, reg) per gap
            'Wad_mean': [],
            'Wad_std':  [],
            'Wad_samples': {f"{g:.3f}": [] for g in D_VALUES},
        }

        n_configs = N_ZSHIFTS * len(ALL_REG)
        idx = 0
        t1 = time.time()
        for iz in range(N_ZSHIFTS):
            se_z = zshift_variant(se_base, iz / N_ZSHIFTS)
            E_se = E_se_per_z[iz]
            for reg_name, shift in ALL_REG:
                idx += 1
                reg_data = {'shift': list(shift), 'curve': {}}
                for d in D_VALUES:
                    d_key = f"{d:.3f}"
                    try:
                        stacked = stack_interface(se_z, ncm, d, shift)
                        stacked.calc = calc
                        E_int = float(stacked.get_potential_energy())
                        A = float(xy_area(stacked.cell.array))
                        # Phase1 formula: Wad = -(E - E_se - E_ncm)/A * 16.0218
                        # = (E_se + E_ncm - E)/A * 16.0218
                        Wad = -(E_int - E_se - E_ncm) / A * 16.0218
                        reg_data['curve'][d_key] = {
                            'E_int': E_int, 'Wad_J_per_m2': Wad, 'area_A2': A
                        }
                        comp_data['Wad_samples'][d_key].append(Wad)
                    except Exception as e:
                        log(f"  FAIL z{iz} {reg_name} d={d:.2f}: {e}")
                        reg_data['curve'][d_key] = {'E_int': None, 'error': str(e)}

                comp_data['Wad_per_z_per_reg'][f"z{iz}"][reg_name] = reg_data
                if idx % 5 == 0 or idx == n_configs:
                    el = time.time() - t1
                    eta = el * (n_configs - idx) / idx
                    log(f"  {c}: config {idx}/{n_configs}  z{iz} {reg_name}  "
                        f"el={el/60:.1f}min ETA={eta/60:.1f}min")
                gc.collect()

        # Aggregate Wad_mean / std per gap (over z × reg)
        for d in D_VALUES:
            d_key = f"{d:.3f}"
            samples = comp_data['Wad_samples'][d_key]
            if samples:
                comp_data['Wad_mean'].append(float(np.mean(samples)))
                comp_data['Wad_std'].append(float(np.std(samples)))
            else:
                comp_data['Wad_mean'].append(None)
                comp_data['Wad_std'].append(None)

        json.dump(comp_data, open(checkpoint, 'w'), indent=2)
        log(f"  saved {checkpoint.name}")

    log(f"\n=== TOTAL: {(time.time()-t_start)/3600:.2f} h ===")


if __name__ == "__main__":
    main()
