"""Phase 2a v26c — MACE-MP-0 cross-check (M4 from v26b, now executable).

User installed MACE in separate conda env "mace". This script runs M4 phase
ONLY: stack each comp + compute Wad with MACE-MP-0, compare with v15 baseline
(UMA-based) and paper exp.

Key contrast:
  - bond density (geometry) is MLIP-INDEPENDENT (same atoms + cutoffs)
  - Wad ENERGY differs between UMA and MACE
  - v9-v12 showed UMA Wad inverted vs paper exp (rigid)
  - M4 question: does MACE give same inversion (method-independent UMA artifact)
    or different ranking (MLIP-specific)?

Run on KISTI:
  conda activate mace
  cd /scratch/x3430a02/kgy/manuscript_support/adhesion_v5_v2
  wget -O phase2a_v26c_mace.py 'https://raw.githubusercontent.com/.../phase2a_v26c_mace.py'
  mkdir -p phase2a_v26c_results
  python3 phase2a_v26c_mace.py 2>&1 | tee phase2a_v26c_results/run.log
"""
import os, json, time, sys, traceback
from pathlib import Path
import numpy as np
from ase.io import read

COMPS = {
    'comp1':  {'se': 'comp1_slab_v2.xyz',            'ncm': 'ncm_7x7x1_3Lconv.xyz', 'gap_eq': 1.2},
    'comp2':  {'se': 'comp2_slab_v2.xyz',            'ncm': 'ncm_7x7x1_3Lconv.xyz', 'gap_eq': 1.2},
    'comp3':  {'se': 'comp3_slab_v1_PRESERVED.xyz',  'ncm': 'ncm_5x5x1_3Lconv.xyz', 'gap_eq': 1.4},
    'comp4':  {'se': 'comp4_slab_v1_PRESERVED.xyz',  'ncm': 'ncm_5x5x1_3Lconv.xyz', 'gap_eq': 1.6},
    'comp5':  {'se': 'comp5_slab_v1_PRESERVED.xyz',  'ncm': 'ncm_5x5x1_3Lconv.xyz', 'gap_eq': 1.6},
    'modelC': {'se': 'modelC_slab_v2_PRESERVED.xyz', 'ncm': 'ncm_5x5x1_3Lconv.xyz', 'gap_eq': 1.2},
}

BOND_CUTOFFS = {
    ('Li', 'O'): 3.0, ('Cl', 'O'): 3.5, ('Br', 'O'): 3.7,
    ('S', 'Li'): 3.0, ('S', 'Ni'): 3.5, ('Li', 'Ni'): 3.5,
}
VACUUM_TOP = 30.0
PAPER_EXP = {'comp1': 194, 'comp2': 180, 'comp3': 316, 'comp4': 298, 'comp5': 249}
PAPER_COMPS = ['comp1', 'comp2', 'comp3', 'comp4', 'comp5']
ALL_COMPS = PAPER_COMPS + ['modelC']
V15_BASELINE_R_CL_O = -0.9136

RESULTS_DIR = Path("phase2a_v26c_results"); RESULTS_DIR.mkdir(exist_ok=True)
LOG_FILE = RESULTS_DIR / "run.log"


def log(msg):
    s = f"[{time.strftime('%H:%M:%S')}] {msg}"
    print(s, flush=True)
    with open(LOG_FILE, 'a') as f:
        f.write(s + "\n")


def stack_rigid(se, ncm, gap, shift_frac=(0.0, 0.0)):
    se_a = se.copy(); ncm_a = ncm.copy()
    nc = se_a.cell.array.copy()
    nc[0] = ncm_a.cell.array[0]; nc[1] = ncm_a.cell.array[1]
    se_a.set_cell(nc, scale_atoms=True)
    dx, dy = shift_frac
    sc = dx * ncm_a.cell.array[0] + dy * ncm_a.cell.array[1]
    se_a.translate([sc[0], sc[1], 0.0])
    se_a.wrap()
    ncm_a.translate([0, 0, -ncm_a.positions[:, 2].min()])
    z_max = ncm_a.positions[:, 2].max()
    s_min = se_a.positions[:, 2].min()
    se_a.translate([0, 0, z_max - s_min + gap])
    combined = ncm_a + se_a
    new_cell = ncm_a.cell.array.copy()
    z_extent = combined.positions[:, 2].max() - combined.positions[:, 2].min()
    new_cell[2] = [0., 0., z_extent + VACUUM_TOP]
    combined.set_cell(new_cell, scale_atoms=False)
    combined.set_pbc([True, True, True])
    return combined, len(ncm_a)


def xy_area(cell):
    return float(abs(np.cross(cell[0], cell[1])[2]))


def count_interface_bonds(stacked, n_ncm, gap_window=4.5):
    syms = stacked.get_chemical_symbols()
    pos = stacked.positions
    ncm_z_max = pos[:n_ncm, 2].max()
    near = [i for i in range(len(stacked)) if abs(pos[i, 2] - ncm_z_max) < gap_window]
    counts = {}
    for (sa, sb), cut in BOND_CUTOFFS.items():
        n_ab = 0
        for i in near:
            if i >= n_ncm and syms[i] == sa:
                for j in near:
                    if j < n_ncm and syms[j] == sb:
                        if stacked.get_distance(i, j, mic=True) < cut:
                            n_ab += 1
            elif i < n_ncm and syms[i] == sa:
                for j in near:
                    if j >= n_ncm and syms[j] == sb:
                        if stacked.get_distance(i, j, mic=True) < cut:
                            n_ab += 1
        counts[f"{sa}-{sb}"] = n_ab
    return counts


def pearson(x, y):
    x = np.asarray(x, float); y = np.asarray(y, float)
    if x.std() == 0 or y.std() == 0:
        return float('nan')
    return float(np.corrcoef(x, y)[0, 1])


def main():
    t0 = time.time()
    log("=" * 70)
    log("v26c — MACE-MP-0 cross-check (M4 phase ONLY)")
    log("=" * 70)

    # Load MACE
    log("Loading MACE-MP-0 medium...")
    try:
        from mace.calculators import mace_mp
        # default_dtype="float64" gives more accurate energies
        # device="cuda" if available, else cpu
        import torch
        device = "cuda" if torch.cuda.is_available() else "cpu"
        log(f"  device: {device}")
        calc = mace_mp(model="medium", dispersion=False, default_dtype="float64", device=device)
        log("  MACE loaded.")
    except Exception as e:
        log(f"  MACE load FAILED: {e}")
        traceback.print_exc(file=sys.stdout)
        return

    energies = {}
    densities = {}
    for c in ALL_COMPS:
        try:
            log(f"\n--- {c}: gap_eq={COMPS[c]['gap_eq']:.1f} A ---")
            se = read(COMPS[c]['se'])
            ncm = read(COMPS[c]['ncm'])
            stacked, n_ncm = stack_rigid(se, ncm, COMPS[c]['gap_eq'])

            # Geometric bond count (matches v15 exactly)
            counts = count_interface_bonds(stacked, n_ncm)
            A = xy_area(stacked.cell.array)
            densities[c] = {k: v / A for k, v in counts.items()}
            log(f"  bonds: Li-O={counts['Li-O']} Cl-O={counts['Cl-O']} Br-O={counts['Br-O']}")

            # Energies via MACE
            t_e = time.time()
            stacked.calc = calc
            E_int = float(stacked.get_potential_energy())
            log(f"  E_int = {E_int:.4f} eV  ({time.time()-t_e:.1f}s)")

            t_e = time.time()
            se_iso = se.copy(); se_iso.calc = calc
            E_se = float(se_iso.get_potential_energy())
            log(f"  E_se  = {E_se:.4f} eV  ({time.time()-t_e:.1f}s)")

            t_e = time.time()
            ncm_iso = ncm.copy(); ncm_iso.calc = calc
            E_ncm = float(ncm_iso.get_potential_energy())
            log(f"  E_ncm = {E_ncm:.4f} eV  ({time.time()-t_e:.1f}s)")

            Wad = (E_se + E_ncm - E_int) / A * 16.0218  # eV/A^2 -> J/m^2
            energies[c] = {'E_int': E_int, 'E_se': E_se, 'E_ncm': E_ncm,
                           'A': A, 'Wad_J_m2': Wad}
            log(f"  Wad(MACE) = {Wad:+.4f} J/m^2")
        except Exception as e:
            log(f"  {c} FAILED: {e}")
            traceback.print_exc(file=sys.stdout)

    # ────────────────────────── R analyses ──────────────────────────
    log("\n" + "=" * 70)
    log("RESULTS: MACE Wad + bond density vs paper exp")
    log("=" * 70)

    log(f"\n{'comp':<8} {'paper':>6} {'Wad_MACE':>12} {'Cl-O dens':>12} {'Li-O dens':>12}")
    for c in ALL_COMPS:
        e = energies.get(c, {})
        d = densities.get(c, {})
        log(f"{c:<8} {PAPER_EXP.get(c, 0):>6} "
            f"{e.get('Wad_J_m2', 0):>+12.4f} "
            f"{d.get('Cl-O', 0):>+12.4f} "
            f"{d.get('Li-O', 0):>+12.4f}")

    paper = [PAPER_EXP[c] for c in PAPER_COMPS]
    if all(c in energies for c in PAPER_COMPS):
        wad = [energies[c]['Wad_J_m2'] for c in PAPER_COMPS]
        R_wad = pearson(wad, paper)
        log(f"\n  R(Wad_MACE vs paper) = {R_wad:+.4f}")
        if R_wad > 0.5:
            log(f"  ⭐ Wad with MACE gives POSITIVE correlation — better than UMA")
        elif R_wad < -0.5:
            log(f"  ⚠ Wad with MACE also INVERTED — confirms energy descriptor unreliable")
        else:
            log(f"  ~ Wad with MACE gives weak correlation (no strong signal)")

    if all(c in densities for c in PAPER_COMPS):
        for bond in ['Li-O', 'Cl-O', 'Br-O']:
            x = [densities[c].get(bond, 0) for c in PAPER_COMPS]
            R = pearson(x, paper)
            log(f"  R({bond} density via MACE-stack) = {R:+.4f}  "
                f"(should equal v15 since geometric)")

    log(f"\n=== v26c DONE: {(time.time()-t0)/60:.1f} min ===")
    json.dump({'energies': energies, 'densities': densities},
              open(RESULTS_DIR / "summary.json", 'w'), indent=2, default=str)


if __name__ == "__main__":
    main()
