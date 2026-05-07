"""Phase 2a v26 — ALL METHODS (M1-M6) integrated stress-test of v15 baseline.

Goal: stress-test the v15 Cl-O density descriptor (R=-0.91) and Li-O
density (R=+0.82) against 6 orthogonal method variations to establish
how robust the family-level adhesion prediction actually is.

Methods (each phase reproduces v15-style bond density + Pearson R):
  M1 NCM facet variation: build (003), (110), (012) via ase.spacegroup.crystal
                          + ase.build.surface, compare with current (104)
  M2 Constrained relax: top 30% SE LBFGS (max 30 steps),
                        NCM + bottom 70% SE FixAtoms (Type-a only)
  M3 Li position variants: shake all Li ±0.2A, 5 random seeds per comp
  M4 MLIP cross-check: MACE-MP-0 instead of UMA on stacked structures
  M5 SE termination: alternate cleave from middle of existing slab (proxy)
  M6 Lateral 2x2 supercell: slab.repeat((2,2,1)) for finite-size check

Each phase outputs:
  - per-comp Cl-O density, Li-O density
  - Pearson R vs paper_exp (n=5)
  - delta vs v15 baseline (R(Cl-O)=-0.914, R(Li-O)=+0.818)

If a method preserves R(Cl-O) within ±0.15, we conclude family-level
prediction is robust to that perturbation. If signs flip, that's a
fragile dimension we must caveat in paper #2.

Inputs: same as v15 (slab xyz files in CWD).
Time estimate: ~60-90 min total on KISTI single-node.
"""
import os, json, time, sys, traceback
from pathlib import Path
import numpy as np
from ase import Atoms
from ase.io import read, write
from ase.constraints import FixAtoms
from ase.optimize import LBFGS

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

V15_BASELINE = {  # for delta-comparison
    'R_Li-O': +0.8175,
    'R_Cl-O': -0.9136,
    'R_Br-O': +0.4028,
}

RESULTS_DIR = Path("phase2a_v26_results"); RESULTS_DIR.mkdir(exist_ok=True)
LOG_FILE = RESULTS_DIR / "run.log"


def log(msg):
    s = f"[{time.strftime('%H:%M:%S')}] {msg}"
    print(s, flush=True)
    with open(LOG_FILE, 'a') as f:
        f.write(s + "\n")


# =====================================================================
# Shared utilities (from v15)
# =====================================================================

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


def pearson_R(comp_to_density):
    """Compute Pearson R between density values and paper_exp (n=5)."""
    x = np.array([comp_to_density[c] for c in PAPER_COMPS])
    y = np.array([PAPER_EXP[c] for c in PAPER_COMPS])
    if x.std() == 0:
        return float('nan')
    return float(np.corrcoef(x, y)[0, 1])


def descriptor_table(densities_per_comp, label):
    """Print per-comp density table and Pearson R vs paper."""
    log(f"\n--- {label}: bond densities (per A^2) ---")
    log(f"{'comp':<8} {'paper':>6} {'Li-O':>10} {'Cl-O':>10} {'Br-O':>10}")
    for c in ALL_COMPS:
        if c not in densities_per_comp:
            continue
        d = densities_per_comp[c]
        paper = PAPER_EXP.get(c, 0)
        log(f"{c:<8} {paper:>6} "
            f"{d.get('Li-O', 0):>+10.4f} "
            f"{d.get('Cl-O', 0):>+10.4f} "
            f"{d.get('Br-O', 0):>+10.4f}")

    R_results = {}
    for bond in ['Li-O', 'Cl-O', 'Br-O']:
        comp_to_dens = {c: densities_per_comp[c].get(bond, 0)
                        for c in PAPER_COMPS if c in densities_per_comp}
        if len(comp_to_dens) < 5:
            log(f"  R({bond}) = N/A (incomplete data)")
            R_results[bond] = None
            continue
        r = pearson_R(comp_to_dens)
        baseline = V15_BASELINE[f'R_{bond}']
        delta = r - baseline
        flag = "OK" if abs(delta) < 0.15 else "DIFF"
        log(f"  R({bond}) = {r:+.4f}  (v15: {baseline:+.4f}, d={delta:+.3f}, {flag})")
        R_results[bond] = r
    return R_results


# =====================================================================
# M1 — NCM facet variation (003, 110, 012 vs current 104)
# =====================================================================

def build_linio2_facet(hkl, n_layers=3, supercell_xy=(5, 5)):
    """Build LiNiO2 slab on given (hkl) facet."""
    from ase.spacegroup import crystal
    from ase.build import surface
    a = 2.879
    c = 14.176
    linio2 = crystal(
        ['Li', 'Ni', 'O'],
        basis=[(0, 0, 0), (0, 0, 0.5), (0, 0, 0.258)],
        spacegroup=166,
        cellpar=[a, a, c, 90, 90, 120],
    )
    slab = surface(linio2, hkl, n_layers, vacuum=0.0)
    slab = slab.repeat((supercell_xy[0], supercell_xy[1], 1))
    slab.center(vacuum=0.0, axis=2)
    return slab


def phase_M1_facets():
    log("\n" + "=" * 70)
    log("M1: NCM facet variation (003, 110, 012)")
    log("=" * 70)

    facets = {'003': (0, 0, 3), '110': (1, 1, 0), '012': (0, 1, 2)}
    out = {}

    for fname, hkl in facets.items():
        log(f"\n--- Facet ({fname}) build ---")
        try:
            ncm_slab = build_linio2_facet(hkl, n_layers=3, supercell_xy=(5, 5))
            log(f"  built: {len(ncm_slab)} atoms, cell xy={ncm_slab.cell.array[0][:2]} / {ncm_slab.cell.array[1][:2]}")
        except Exception as e:
            log(f"  build FAILED: {e}")
            out[fname] = {'error': str(e)}
            continue

        densities = {}
        for c in ALL_COMPS:
            try:
                se = read(COMPS[c]['se'])
                stacked, n_ncm = stack_rigid(se, ncm_slab, COMPS[c]['gap_eq'])
                counts = count_interface_bonds(stacked, n_ncm)
                A = xy_area(stacked.cell.array)
                densities[c] = {k: v / A for k, v in counts.items()}
            except Exception as e:
                log(f"  {c} stack/count FAILED: {e}")

        R = descriptor_table(densities, f"M1 facet ({fname})")
        out[fname] = {'R': R, 'densities': densities}
    return out


# =====================================================================
# M2 — Constrained relax (Type-a only)
# =====================================================================

def get_uma_calc():
    """Return UMA calculator (cached)."""
    from fairchem.core import OCPCalculator
    return OCPCalculator(model_name="uma-s-1p2", local_cache="/tmp/fairchem_cache", cpu=False)


def phase_M2_constrained_relax():
    log("\n" + "=" * 70)
    log("M2: Constrained relax (top 30% of SE, NCM+bottom fixed)")
    log("=" * 70)

    try:
        calc = get_uma_calc()
    except Exception as e:
        log(f"  UMA calc UNAVAILABLE: {e}")
        return {'error': 'UMA unavailable'}

    densities = {}
    rms_displacements = {}
    for c in ALL_COMPS:
        try:
            se = read(COMPS[c]['se'])
            ncm = read(COMPS[c]['ncm'])
            stacked, n_ncm = stack_rigid(se, ncm, COMPS[c]['gap_eq'])
            n_total = len(stacked)
            n_se = n_total - n_ncm

            # Bottom 70% of SE = fixed; top 30% free
            se_z = stacked.positions[n_ncm:, 2]
            z_min, z_max = se_z.min(), se_z.max()
            z_threshold = z_min + 0.7 * (z_max - z_min)

            fix_idx = list(range(n_ncm))  # all NCM
            for i in range(n_ncm, n_total):
                if stacked.positions[i, 2] < z_threshold:
                    fix_idx.append(i)
            n_free = n_total - len(fix_idx)
            log(f"\n--- {c}: total={n_total}, NCM={n_ncm}, SE_free={n_free}/{n_se} (top {100*n_free/n_se:.0f}%) ---")

            stacked.set_constraint(FixAtoms(indices=fix_idx))
            stacked.calc = calc

            pos_initial = stacked.positions.copy()
            opt = LBFGS(stacked, logfile=str(RESULTS_DIR / f"m2_{c}.log"))
            opt.run(fmax=0.1, steps=30)
            pos_final = stacked.positions.copy()

            disp = pos_final - pos_initial
            rms = np.sqrt(np.mean(np.sum(disp**2, axis=1)))
            max_disp = np.sqrt(np.max(np.sum(disp**2, axis=1)))
            rms_displacements[c] = {'rms': float(rms), 'max': float(max_disp)}
            log(f"  RMS disp = {rms:.3f} A, max = {max_disp:.3f} A")

            stacked.set_constraint(None)
            counts = count_interface_bonds(stacked, n_ncm)
            A = xy_area(stacked.cell.array)
            densities[c] = {k: v / A for k, v in counts.items()}
            log(f"  bonds: Li-O={counts['Li-O']} Cl-O={counts['Cl-O']} Br-O={counts['Br-O']}")
        except Exception as e:
            log(f"  {c} FAILED: {e}")
            traceback.print_exc(file=sys.stdout)

    R = descriptor_table(densities, "M2 constrained-relax")
    return {'R': R, 'densities': densities, 'rms': rms_displacements}


# =====================================================================
# M3 — Li position shake variants (5 seeds per comp)
# =====================================================================

def phase_M3_li_shake():
    log("\n" + "=" * 70)
    log("M3: Li position shake (+/- 0.2 A, 5 seeds per comp)")
    log("=" * 70)

    SHAKE_AMP = 0.2
    N_SEEDS = 5

    seed_results = {seed: {} for seed in range(N_SEEDS)}
    for c in ALL_COMPS:
        for seed in range(N_SEEDS):
            try:
                se = read(COMPS[c]['se'])
                ncm = read(COMPS[c]['ncm'])
                rng = np.random.default_rng(seed * 100 + hash(c) % 1000)
                syms = se.get_chemical_symbols()
                li_idx = [i for i, s in enumerate(syms) if s == 'Li']
                shake = rng.normal(0, SHAKE_AMP, (len(li_idx), 3))
                se.positions[li_idx] += shake

                stacked, n_ncm = stack_rigid(se, ncm, COMPS[c]['gap_eq'])
                counts = count_interface_bonds(stacked, n_ncm)
                A = xy_area(stacked.cell.array)
                seed_results[seed][c] = {k: v / A for k, v in counts.items()}
            except Exception as e:
                log(f"  {c} seed={seed} FAILED: {e}")

    # Per-seed R
    log(f"\n--- Per-seed Pearson R (Li shake +/- {SHAKE_AMP} A) ---")
    log(f"{'seed':<6} {'R(Li-O)':>10} {'R(Cl-O)':>10} {'R(Br-O)':>10}")
    R_per_seed = {}
    for seed in range(N_SEEDS):
        d = seed_results[seed]
        R = {}
        for bond in ['Li-O', 'Cl-O', 'Br-O']:
            comp_to_dens = {c: d[c].get(bond, 0) for c in PAPER_COMPS if c in d}
            R[bond] = pearson_R(comp_to_dens) if len(comp_to_dens) == 5 else float('nan')
        R_per_seed[seed] = R
        log(f"  {seed:<6} {R['Li-O']:>+10.4f} {R['Cl-O']:>+10.4f} {R['Br-O']:>+10.4f}")

    # Mean +/- std of R
    log(f"\n--- R statistics across 5 seeds ---")
    for bond in ['Li-O', 'Cl-O', 'Br-O']:
        rs = [R_per_seed[s][bond] for s in range(N_SEEDS) if not np.isnan(R_per_seed[s][bond])]
        if rs:
            log(f"  R({bond}) = {np.mean(rs):+.4f} +/- {np.std(rs):.4f}  "
                f"(v15: {V15_BASELINE[f'R_{bond}']:+.4f})")
    return {'R_per_seed': R_per_seed, 'seed_densities': seed_results}


# =====================================================================
# M4 — MLIP cross-check (MACE-MP-0)
# =====================================================================

def phase_M4_mace_check():
    log("\n" + "=" * 70)
    log("M4: MLIP cross-check (MACE-MP-0)")
    log("=" * 70)

    try:
        from mace.calculators import mace_mp
        calc = mace_mp(model="medium", dispersion=False, default_dtype="float64")
        log("  MACE-MP-0 medium loaded")
    except Exception as e:
        log(f"  MACE UNAVAILABLE: {e}")
        log(f"  M4 SKIPPED — MACE not installed in this env")
        return {'error': 'MACE unavailable'}

    # Compute energies + bond counts at gap_eq with MACE.
    # Note: M4 is mainly to verify that energy ranking is method-dependent;
    # bond count is geometric (independent of MLIP) so should match v15 exactly.
    energies = {}
    densities = {}
    for c in ALL_COMPS:
        try:
            se = read(COMPS[c]['se'])
            ncm = read(COMPS[c]['ncm'])
            stacked, n_ncm = stack_rigid(se, ncm, COMPS[c]['gap_eq'])
            stacked.calc = calc
            E_int = float(stacked.get_potential_energy())

            se_iso = se.copy(); se_iso.calc = calc
            ncm_iso = ncm.copy(); ncm_iso.calc = calc
            E_se = float(se_iso.get_potential_energy())
            E_ncm = float(ncm_iso.get_potential_energy())

            A = xy_area(stacked.cell.array)
            Wad_mace = (E_se + E_ncm - E_int) / A * 16.0218
            energies[c] = {'E_int': E_int, 'E_se': E_se, 'E_ncm': E_ncm, 'A': A, 'Wad': Wad_mace}
            counts = count_interface_bonds(stacked, n_ncm)
            densities[c] = {k: v / A for k, v in counts.items()}
            log(f"  {c}: Wad(MACE)={Wad_mace:+.4f} J/m^2")
        except Exception as e:
            log(f"  {c} FAILED: {e}")

    # R(Wad_MACE) vs paper
    if all(c in energies for c in PAPER_COMPS):
        wad = {c: energies[c]['Wad'] for c in PAPER_COMPS}
        R_wad = pearson_R(wad)
        log(f"\n  R(Wad_MACE vs paper) = {R_wad:+.4f}")

    # R(bond density via MACE structures — should match v15 exactly since geom is same)
    R_bond = descriptor_table(densities, "M4 MACE bond-count")
    return {'energies': energies, 'densities': densities, 'R_bond': R_bond}


# =====================================================================
# M5 — SE termination (proxy: extract bulk from middle of slab, re-cleave)
# =====================================================================

def phase_M5_se_termination():
    log("\n" + "=" * 70)
    log("M5: SE termination variation (proxy: middle-extract + re-stack)")
    log("=" * 70)
    log("  Method: take middle ~40% of each SE slab as 'bulk-like' region,")
    log("  re-stack with NCM. Tests if surface termination of current slab")
    log("  is the dominant signal vs deeper SE chemistry.")

    densities = {}
    for c in ALL_COMPS:
        try:
            se = read(COMPS[c]['se'])
            ncm = read(COMPS[c]['ncm'])
            z = se.positions[:, 2]
            z_min, z_max = z.min(), z.max()
            mid_lo = z_min + 0.30 * (z_max - z_min)
            mid_hi = z_min + 0.70 * (z_max - z_min)
            keep = [i for i in range(len(se)) if mid_lo <= z[i] <= mid_hi]
            se_mid = se[keep]
            log(f"\n--- {c}: original {len(se)} atoms, middle-region {len(se_mid)} atoms ---")
            if len(se_mid) < 10:
                log(f"  too few atoms after extract; skip")
                continue
            # Recenter, give vacuum
            se_mid.center(vacuum=0.0, axis=2)
            stacked, n_ncm = stack_rigid(se_mid, ncm, COMPS[c]['gap_eq'])
            counts = count_interface_bonds(stacked, n_ncm)
            A = xy_area(stacked.cell.array)
            densities[c] = {k: v / A for k, v in counts.items()}
        except Exception as e:
            log(f"  {c} FAILED: {e}")

    R = descriptor_table(densities, "M5 middle-extract termination")
    return {'R': R, 'densities': densities}


# =====================================================================
# M6 — Lateral 2x2 supercell (finite-size check)
# =====================================================================

def phase_M6_lateral_supercell():
    log("\n" + "=" * 70)
    log("M6: Lateral 2x2 supercell (finite-size check)")
    log("=" * 70)
    log("  Method: stack as v15, then stacked.repeat((2,2,1)). If bond")
    log("  density (per area) unchanged, no finite-size effect. If changed,")
    log("  current cell suffers periodic-image artifact.")

    densities_1x1 = {}
    densities_2x2 = {}
    for c in ALL_COMPS:
        try:
            se = read(COMPS[c]['se'])
            ncm = read(COMPS[c]['ncm'])

            # 1x1 baseline
            stacked, n_ncm = stack_rigid(se, ncm, COMPS[c]['gap_eq'])
            counts1 = count_interface_bonds(stacked, n_ncm)
            A1 = xy_area(stacked.cell.array)
            densities_1x1[c] = {k: v / A1 for k, v in counts1.items()}

            # 2x2: just repeat the entire stacked slab
            stacked2 = stacked.repeat((2, 2, 1))
            n_ncm2 = n_ncm * 4
            counts2 = count_interface_bonds(stacked2, n_ncm2)
            A2 = xy_area(stacked2.cell.array)
            densities_2x2[c] = {k: v / A2 for k, v in counts2.items()}

            log(f"  {c}: 1x1 area={A1:.1f} A^2, 2x2 area={A2:.1f} A^2 (ratio={A2/A1:.2f})")
            for bond in ['Li-O', 'Cl-O', 'Br-O']:
                d1 = densities_1x1[c][bond]
                d2 = densities_2x2[c][bond]
                ddiff = d2 - d1
                log(f"    {bond}: dens 1x1={d1:+.4f}  2x2={d2:+.4f}  delta={ddiff:+.4f}")
        except Exception as e:
            log(f"  {c} FAILED: {e}")

    log(f"\n--- 1x1 baseline ---")
    R1 = descriptor_table(densities_1x1, "M6 (1x1 baseline)")
    log(f"\n--- 2x2 supercell ---")
    R2 = descriptor_table(densities_2x2, "M6 (2x2 supercell)")
    return {'R_1x1': R1, 'R_2x2': R2, 'd_1x1': densities_1x1, 'd_2x2': densities_2x2}


# =====================================================================
# Main driver
# =====================================================================

def main():
    t0 = time.time()
    log("=" * 70)
    log("v26 — ALL METHODS (M1-M6) integrated stress-test")
    log("=" * 70)
    log(f"v15 baseline: R(Li-O)={V15_BASELINE['R_Li-O']:+.4f}, "
        f"R(Cl-O)={V15_BASELINE['R_Cl-O']:+.4f}, "
        f"R(Br-O)={V15_BASELINE['R_Br-O']:+.4f}")

    summary = {}

    for label, fn in [
        ('M1_facets', phase_M1_facets),
        ('M2_constrained', phase_M2_constrained_relax),
        ('M3_li_shake', phase_M3_li_shake),
        ('M4_mace', phase_M4_mace_check),
        ('M5_termination', phase_M5_se_termination),
        ('M6_lateral_2x2', phase_M6_lateral_supercell),
    ]:
        t_phase = time.time()
        log(f"\n##### {label} START at t+{(t_phase-t0)/60:.1f} min #####")
        try:
            summary[label] = fn()
        except Exception as e:
            log(f"  {label} FATAL: {e}")
            traceback.print_exc(file=sys.stdout)
            summary[label] = {'fatal': str(e)}
        log(f"##### {label} DONE in {(time.time()-t_phase)/60:.1f} min #####")

    # =========================================================
    # Final summary table
    # =========================================================
    log("\n" + "=" * 70)
    log("FINAL SUMMARY: R(Cl-O) and R(Li-O) across all methods")
    log("=" * 70)
    log(f"{'method':<25} {'R(Li-O)':>10} {'R(Cl-O)':>10} {'R(Br-O)':>10}")
    log(f"{'v15 baseline':<25} {V15_BASELINE['R_Li-O']:>+10.4f} "
        f"{V15_BASELINE['R_Cl-O']:>+10.4f} {V15_BASELINE['R_Br-O']:>+10.4f}")

    def rget(d, bond):
        if not isinstance(d, dict):
            return None
        if 'R' in d and isinstance(d['R'], dict):
            return d['R'].get(bond)
        if 'R_bond' in d and isinstance(d['R_bond'], dict):
            return d['R_bond'].get(bond)
        return None

    # M1 (per facet)
    if isinstance(summary.get('M1_facets'), dict):
        for fname, fdat in summary['M1_facets'].items():
            label = f"M1_facet_({fname})"
            r_li = rget(fdat, 'Li-O'); r_cl = rget(fdat, 'Cl-O'); r_br = rget(fdat, 'Br-O')
            if all(x is not None for x in (r_li, r_cl, r_br)):
                log(f"{label:<25} {r_li:>+10.4f} {r_cl:>+10.4f} {r_br:>+10.4f}")

    # M2
    r_li = rget(summary.get('M2_constrained'), 'Li-O')
    r_cl = rget(summary.get('M2_constrained'), 'Cl-O')
    r_br = rget(summary.get('M2_constrained'), 'Br-O')
    if all(x is not None for x in (r_li, r_cl, r_br)):
        log(f"{'M2_constrained_relax':<25} {r_li:>+10.4f} {r_cl:>+10.4f} {r_br:>+10.4f}")

    # M3 (mean of 5 seeds)
    if isinstance(summary.get('M3_li_shake'), dict) and 'R_per_seed' in summary['M3_li_shake']:
        rps = summary['M3_li_shake']['R_per_seed']
        for bond_idx, bond in enumerate(['Li-O', 'Cl-O', 'Br-O']):
            pass  # already logged in phase
        means = {}
        for bond in ['Li-O', 'Cl-O', 'Br-O']:
            vals = [rps[s][bond] for s in rps if not np.isnan(rps[s][bond])]
            means[bond] = np.mean(vals) if vals else float('nan')
        log(f"{'M3_li_shake (mean 5)':<25} {means['Li-O']:>+10.4f} "
            f"{means['Cl-O']:>+10.4f} {means['Br-O']:>+10.4f}")

    # M4
    r_li = rget(summary.get('M4_mace'), 'Li-O')
    r_cl = rget(summary.get('M4_mace'), 'Cl-O')
    r_br = rget(summary.get('M4_mace'), 'Br-O')
    if all(x is not None for x in (r_li, r_cl, r_br)):
        log(f"{'M4_MACE_geom':<25} {r_li:>+10.4f} {r_cl:>+10.4f} {r_br:>+10.4f}")

    # M5
    r_li = rget(summary.get('M5_termination'), 'Li-O')
    r_cl = rget(summary.get('M5_termination'), 'Cl-O')
    r_br = rget(summary.get('M5_termination'), 'Br-O')
    if all(x is not None for x in (r_li, r_cl, r_br)):
        log(f"{'M5_middle_extract':<25} {r_li:>+10.4f} {r_cl:>+10.4f} {r_br:>+10.4f}")

    # M6
    if isinstance(summary.get('M6_lateral_2x2'), dict):
        for tag, key in [('M6_1x1_recheck', 'R_1x1'), ('M6_2x2_supercell', 'R_2x2')]:
            r_li = summary['M6_lateral_2x2'].get(key, {}).get('Li-O')
            r_cl = summary['M6_lateral_2x2'].get(key, {}).get('Cl-O')
            r_br = summary['M6_lateral_2x2'].get(key, {}).get('Br-O')
            if all(x is not None for x in (r_li, r_cl, r_br)):
                log(f"{tag:<25} {r_li:>+10.4f} {r_cl:>+10.4f} {r_br:>+10.4f}")

    # Verdict
    log(f"\n--- VERDICT ---")
    log(f"Cl-O sign-stability across methods is the key robustness criterion.")
    log(f"If R(Cl-O) stays in [-1.0, -0.7] across all methods: family-level")
    log(f"prediction is method-independent. If sign flips for any method,")
    log(f"that perturbation breaks the descriptor and must be caveated.")

    log(f"\n=== v26 DONE: total {(time.time()-t0)/60:.1f} min ===")
    json.dump(summary, open(RESULTS_DIR / "summary.json", 'w'), indent=2, default=str)


if __name__ == "__main__":
    main()
