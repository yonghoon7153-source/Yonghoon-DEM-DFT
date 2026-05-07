"""Phase 2a v26b — patch for v26: fix M2 (UMA import) + M6 (2x2 supercell).

v26 results showed:
  - M1 facets, M3 Li shake: R(Cl-O) ~ -0.91 robust ✓
  - M5 middle-extract: R weakened (termination matters)
  - M2 FAILED: 'OCPCalculator' import error → use FAIRChemCalculator (v23 pattern)
  - M6 BROKEN: ase.repeat((2,2,1)) reorders atoms; n_ncm*4 wrong

This patch reruns ONLY M2 and M6 with fixes:
  - M2: from fairchem.core.calculate.ase_calculator import FAIRChemCalculator,
        pred = pretrained_mlip.get_predict_unit("uma-s-1p1", device="cuda")
  - M6: repeat NCM and SE separately first, THEN stack — preserves index split

Outputs to phase2a_v26_results/ to merge with existing run.log.
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

V15_BASELINE = {'R_Li-O': +0.8175, 'R_Cl-O': -0.9136, 'R_Br-O': +0.4028}

RESULTS_DIR = Path("phase2a_v26_results"); RESULTS_DIR.mkdir(exist_ok=True)
LOG_FILE = RESULTS_DIR / "v26b_patch.log"


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


def pearson_R(comp_to_density):
    x = np.array([comp_to_density[c] for c in PAPER_COMPS])
    y = np.array([PAPER_EXP[c] for c in PAPER_COMPS])
    if x.std() == 0:
        return float('nan')
    return float(np.corrcoef(x, y)[0, 1])


def descriptor_table(densities_per_comp, label):
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
            R_results[bond] = None; continue
        r = pearson_R(comp_to_dens)
        baseline = V15_BASELINE[f'R_{bond}']
        delta = r - baseline
        flag = "OK" if abs(delta) < 0.15 else "DIFF"
        log(f"  R({bond}) = {r:+.4f}  (v15: {baseline:+.4f}, d={delta:+.3f}, {flag})")
        R_results[bond] = r
    return R_results


# =====================================================================
# M2 fixed — use v23 import pattern
# =====================================================================

def get_uma_calc():
    from fairchem.core import pretrained_mlip
    from fairchem.core.calculate.ase_calculator import FAIRChemCalculator
    pred = pretrained_mlip.get_predict_unit("uma-s-1p1", device="cuda")
    return FAIRChemCalculator(pred, task_name="omat")


def phase_M2_constrained_relax():
    log("\n" + "=" * 70)
    log("M2 (FIXED): Constrained relax (top 30% of SE, NCM+bottom fixed)")
    log("=" * 70)

    try:
        log("  Loading UMA via FAIRChemCalculator...")
        calc = get_uma_calc()
        log("  UMA loaded.")
    except Exception as e:
        log(f"  UMA still unavailable: {e}")
        traceback.print_exc(file=sys.stdout)
        return {'error': str(e)}

    densities = {}
    rms_displacements = {}
    for c in ALL_COMPS:
        try:
            se = read(COMPS[c]['se'])
            ncm = read(COMPS[c]['ncm'])
            stacked, n_ncm = stack_rigid(se, ncm, COMPS[c]['gap_eq'])
            n_total = len(stacked)
            n_se = n_total - n_ncm

            se_z = stacked.positions[n_ncm:, 2]
            z_min, z_max = se_z.min(), se_z.max()
            z_threshold = z_min + 0.7 * (z_max - z_min)

            fix_idx = list(range(n_ncm))
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
            if rms > 1.5:
                log(f"  WARNING: RMS > 1.5 A — possible Li migration despite FixAtoms")

            stacked.set_constraint(None)
            counts = count_interface_bonds(stacked, n_ncm)
            A = xy_area(stacked.cell.array)
            densities[c] = {k: v / A for k, v in counts.items()}
            log(f"  bonds: Li-O={counts['Li-O']} Cl-O={counts['Cl-O']} Br-O={counts['Br-O']}")
        except Exception as e:
            log(f"  {c} FAILED: {e}")
            traceback.print_exc(file=sys.stdout)

    R = descriptor_table(densities, "M2 constrained-relax (FIXED)")
    return {'R': R, 'densities': densities, 'rms': rms_displacements}


# =====================================================================
# M6 fixed — repeat NCM and SE separately BEFORE stacking
# =====================================================================

def phase_M6_lateral_supercell():
    log("\n" + "=" * 70)
    log("M6 (FIXED): Lateral 2x2 supercell (repeat NCM + SE separately, then stack)")
    log("=" * 70)

    densities_1x1 = {}
    densities_2x2 = {}
    for c in ALL_COMPS:
        try:
            se = read(COMPS[c]['se'])
            ncm = read(COMPS[c]['ncm'])

            # 1x1 baseline (sanity)
            stacked1, n_ncm1 = stack_rigid(se, ncm, COMPS[c]['gap_eq'])
            counts1 = count_interface_bonds(stacked1, n_ncm1)
            A1 = xy_area(stacked1.cell.array)
            densities_1x1[c] = {k: v / A1 for k, v in counts1.items()}

            # 2x2: repeat each component separately, then stack
            se2 = se.repeat((2, 2, 1))
            ncm2 = ncm.repeat((2, 2, 1))
            stacked2, n_ncm2 = stack_rigid(se2, ncm2, COMPS[c]['gap_eq'])
            counts2 = count_interface_bonds(stacked2, n_ncm2)
            A2 = xy_area(stacked2.cell.array)
            densities_2x2[c] = {k: v / A2 for k, v in counts2.items()}

            log(f"  {c}: 1x1 area={A1:.1f} (n={len(stacked1)}), "
                f"2x2 area={A2:.1f} (n={len(stacked2)}, ratio={A2/A1:.2f})")
            for bond in ['Li-O', 'Cl-O', 'Br-O']:
                d1 = densities_1x1[c][bond]
                d2 = densities_2x2[c][bond]
                rel = (d2 - d1) / d1 * 100 if d1 != 0 else 0.0
                log(f"    {bond}: 1x1={d1:+.4f}  2x2={d2:+.4f}  rel_diff={rel:+.1f}%")
        except Exception as e:
            log(f"  {c} FAILED: {e}")

    log(f"\n--- 1x1 baseline (sanity) ---")
    R1 = descriptor_table(densities_1x1, "M6 (1x1 baseline)")
    log(f"\n--- 2x2 supercell ---")
    R2 = descriptor_table(densities_2x2, "M6 (2x2 supercell, FIXED)")
    return {'R_1x1': R1, 'R_2x2': R2, 'd_1x1': densities_1x1, 'd_2x2': densities_2x2}


# =====================================================================
# Main
# =====================================================================

def main():
    t0 = time.time()
    log("=" * 70)
    log("v26b — patch for M2 (UMA fix) + M6 (supercell fix)")
    log("=" * 70)

    summary = {}
    for label, fn in [
        ('M2_constrained_FIXED', phase_M2_constrained_relax),
        ('M6_lateral_2x2_FIXED', phase_M6_lateral_supercell),
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

    # Combined summary including v26 results
    log("\n" + "=" * 70)
    log("UPDATED FULL SUMMARY (v26 + v26b patch)")
    log("=" * 70)
    log(f"{'method':<28} {'R(Li-O)':>10} {'R(Cl-O)':>10} {'R(Br-O)':>10}")
    log(f"{'v15 baseline':<28} {V15_BASELINE['R_Li-O']:>+10.4f} "
        f"{V15_BASELINE['R_Cl-O']:>+10.4f} {V15_BASELINE['R_Br-O']:>+10.4f}")
    log(f"{'M1_facet_(003)':<28} {-0.6161:>+10.4f} {-0.9141:>+10.4f} {+0.4028:>+10.4f}")
    log(f"{'M1_facet_(110)':<28} {-0.7855:>+10.4f} {-0.9107:>+10.4f} {+0.4038:>+10.4f}")
    log(f"{'M1_facet_(012)':<28} {-0.7889:>+10.4f} {-0.9121:>+10.4f} {+0.4023:>+10.4f}")
    log(f"{'M3_li_shake (mean 5)':<28} {-0.1050:>+10.4f} {-0.8863:>+10.4f} {+0.4028:>+10.4f}")
    log(f"{'M5_middle_extract':<28} {-0.0765:>+10.4f} {-0.4930:>+10.4f} {-0.6223:>+10.4f}")

    def rget(d, bond):
        if not isinstance(d, dict): return None
        if 'R' in d and isinstance(d['R'], dict):
            return d['R'].get(bond)
        return None

    m2 = summary.get('M2_constrained_FIXED', {})
    if isinstance(m2, dict):
        rli = rget(m2, 'Li-O'); rcl = rget(m2, 'Cl-O'); rbr = rget(m2, 'Br-O')
        if all(x is not None for x in (rli, rcl, rbr)):
            log(f"{'M2_constrained (FIXED)':<28} {rli:>+10.4f} {rcl:>+10.4f} {rbr:>+10.4f}")

    m6 = summary.get('M6_lateral_2x2_FIXED', {})
    if isinstance(m6, dict):
        for tag, key in [('M6_1x1_recheck', 'R_1x1'), ('M6_2x2 (FIXED)', 'R_2x2')]:
            rdict = m6.get(key) or {}
            rli = rdict.get('Li-O'); rcl = rdict.get('Cl-O'); rbr = rdict.get('Br-O')
            if all(x is not None for x in (rli, rcl, rbr)):
                log(f"{tag:<28} {rli:>+10.4f} {rcl:>+10.4f} {rbr:>+10.4f}")

    log(f"\n=== v26b DONE: total {(time.time()-t0)/60:.1f} min ===")
    json.dump(summary, open(RESULTS_DIR / "v26b_summary.json", 'w'), indent=2, default=str)


if __name__ == "__main__":
    main()
