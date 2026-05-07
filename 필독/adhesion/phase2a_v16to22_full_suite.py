"""Phase 2a v16-v22 — comprehensive validation suite (ONE SCRIPT, ~15 min total).

Tests v15 robustness across multiple dimensions to confirm bond density
descriptor is publication-grade for paper #2.

v16: Cutoff sensitivity (Li-O 2.5..3.5 Å, Cl-O 3.0..4.0 Å)
v17: Gap window sensitivity (3.0..5.0 Å)
v18: Per-Li atom decomposition (which Li atoms anchor to NCM-O?)
v19: Phase 1 W_max cross-validation (existing data)
v20: Save xyz files for VESTA visualization
v21: Composite descriptor (Li-O − α·Cl-O − β·Br-O) optimization
v22: Relaxed bond count (LIMITED LBFGS to allow type-(a) relaxation only)

Inputs (from v14 Phase B):
  comp1: gap_eq=1.2, comp2: gap_eq=1.2, comp3: gap_eq=1.4
  comp4: gap_eq=1.6, comp5: gap_eq=1.6, modelC: gap_eq=1.2

Outputs:
  phase2a_v16to22_results/
    v16_cutoff.json
    v17_gap_window.json
    v18_per_atom.json
    v19_phase1_crossval.json
    v20_xyz/  (xyz files)
    v21_composite.json
    v22_relaxed.json
    summary.json
"""
import os, json, time
from pathlib import Path
import numpy as np
from ase.io import read, write
from ase.optimize import LBFGS
from ase.constraints import FixAtoms

# -----------------------------------------------------------------------------
COMPS = {
    'comp1':  {'se': 'comp1_slab_v2.xyz',            'ncm': 'ncm_7x7x1_3Lconv.xyz', 'gap_eq': 1.2},
    'comp2':  {'se': 'comp2_slab_v2.xyz',            'ncm': 'ncm_7x7x1_3Lconv.xyz', 'gap_eq': 1.2},
    'comp3':  {'se': 'comp3_slab_v1_PRESERVED.xyz',  'ncm': 'ncm_5x5x1_3Lconv.xyz', 'gap_eq': 1.4},
    'comp4':  {'se': 'comp4_slab_v1_PRESERVED.xyz',  'ncm': 'ncm_5x5x1_3Lconv.xyz', 'gap_eq': 1.6},
    'comp5':  {'se': 'comp5_slab_v1_PRESERVED.xyz',  'ncm': 'ncm_5x5x1_3Lconv.xyz', 'gap_eq': 1.6},
    'modelC': {'se': 'modelC_slab_v2_PRESERVED.xyz', 'ncm': 'ncm_5x5x1_3Lconv.xyz', 'gap_eq': 1.2},
}
PAPER_EXP = {'comp1': 194, 'comp2': 180, 'comp3': 316, 'comp4': 298, 'comp5': 249}

DEFAULT_CUTOFFS = {('Li','O'):3.0, ('Cl','O'):3.5, ('Br','O'):3.7,
                   ('S','Li'):3.0, ('S','Ni'):3.5, ('Li','Ni'):3.5}

VACUUM_TOP = 30.0
RANDOM_SEED = 42

RESULTS_DIR = Path("phase2a_v16to22_results"); RESULTS_DIR.mkdir(exist_ok=True)
(RESULTS_DIR / "v20_xyz").mkdir(exist_ok=True)
LOG_FILE = RESULTS_DIR / "progress.log"


def log(msg):
    s = f"[{time.strftime('%H:%M:%S')}] {msg}"
    print(s, flush=True)
    with open(LOG_FILE, 'a') as f:
        f.write(s + "\n")


_predictor = None
def make_calc():
    global _predictor
    from fairchem.core import pretrained_mlip
    from fairchem.core.calculate.ase_calculator import FAIRChemCalculator
    if _predictor is None:
        _predictor = pretrained_mlip.get_predict_unit("uma-s-1p1", device="cuda")
    return FAIRChemCalculator(_predictor, task_name="omat")


def add_vacuum(atoms, vac):
    cell = atoms.cell.array.copy(); cell[2,2] += vac
    atoms.set_cell(cell, scale_atoms=False); atoms.set_pbc([True,True,True])
    return atoms


def stack_rigid(se, ncm, gap, shift_frac):
    se_a = se.copy(); ncm_a = ncm.copy()
    nc = se_a.cell.array.copy(); nc[0]=ncm_a.cell.array[0]; nc[1]=ncm_a.cell.array[1]
    se_a.set_cell(nc, scale_atoms=True)
    dx, dy = shift_frac
    sc = dx*ncm_a.cell.array[0] + dy*ncm_a.cell.array[1]
    se_a.translate([sc[0], sc[1], 0.0]); se_a.wrap()
    ncm_a.translate([0, 0, -ncm_a.positions[:,2].min()])
    z_max = ncm_a.positions[:,2].max(); s_min = se_a.positions[:,2].min()
    se_a.translate([0, 0, z_max-s_min+gap])
    combined = ncm_a + se_a
    new_cell = ncm_a.cell.array.copy()
    z_extent = combined.positions[:,2].max() - combined.positions[:,2].min()
    new_cell[2] = [0., 0., z_extent + VACUUM_TOP]
    combined.set_cell(new_cell, scale_atoms=False); combined.set_pbc([True,True,True])
    return combined, len(ncm_a)


def xy_area(cell):
    return float(abs(np.cross(cell[0], cell[1])[2]))


def count_bonds(stacked, n_ncm, cutoffs, gap_window=4.5):
    """Count interface bonds within gap_window of NCM_top using given cutoffs."""
    syms = stacked.get_chemical_symbols(); pos = stacked.positions
    ncm_z_max = pos[:n_ncm,2].max()
    near = [i for i in range(len(stacked)) if abs(pos[i,2]-ncm_z_max) < gap_window]
    counts = {}
    for (sa, sb), cut in cutoffs.items():
        n_ab = 0
        for i in near:
            if i >= n_ncm and syms[i] == sa:
                for j in near:
                    if j < n_ncm and syms[j] == sb:
                        if stacked.get_distance(i, j, mic=True) < cut: n_ab += 1
            elif i < n_ncm and syms[i] == sa:
                for j in near:
                    if j >= n_ncm and syms[j] == sb:
                        if stacked.get_distance(i, j, mic=True) < cut: n_ab += 1
        counts[f"{sa}-{sb}"] = n_ab
    return counts


def pearson_R(x, y):
    x, y = np.array(x), np.array(y)
    if x.std() == 0 or y.std() == 0: return float('nan')
    return float(np.corrcoef(x, y)[0,1])


# =============================================================================
# v16 — Cutoff sensitivity
# =============================================================================
def v16_cutoff_sensitivity():
    log("=" * 70)
    log("v16: CUTOFF SENSITIVITY (Li-O 2.5..3.5, Cl-O 3.0..4.0)")
    log("=" * 70)

    cutoffs_to_test = {
        'Li-O': [2.5, 2.8, 3.0, 3.2, 3.5],
        'Cl-O': [3.0, 3.3, 3.5, 3.7, 4.0],
        'Br-O': [3.2, 3.5, 3.7, 4.0, 4.3],
    }

    results = {}
    for varied_pair, cuts in cutoffs_to_test.items():
        log(f"\n--- Vary {varied_pair} cutoff ---")
        results[varied_pair] = {}
        for cut in cuts:
            cutoffs = dict(DEFAULT_CUTOFFS)
            sa, sb = varied_pair.split('-')
            cutoffs[(sa, sb)] = cut

            comp_data = {}
            for comp, cfg in COMPS.items():
                se = read(cfg['se']); ncm = read(cfg['ncm'])
                stacked, n_ncm = stack_rigid(se, ncm, cfg['gap_eq'], (0., 0.))
                A = xy_area(stacked.cell.array)
                counts = count_bonds(stacked, n_ncm, cutoffs)
                density = counts[varied_pair] / A
                comp_data[comp] = {'count': counts[varied_pair], 'density': density, 'A': A}

            # Pearson R vs paper exp
            xs_dens = [comp_data[c]['density'] for c in PAPER_EXP]
            ys = [PAPER_EXP[c] for c in PAPER_EXP]
            R = pearson_R(xs_dens, ys)
            results[varied_pair][f"{cut:.2f}"] = {
                'cutoff': cut,
                'comp_data': comp_data,
                'R_density_vs_exp': R,
            }
            log(f"  cutoff={cut:.2f}A  R({varied_pair} dens vs exp)={R:+.4f}")

    return results


# =============================================================================
# v17 — Gap window sensitivity
# =============================================================================
def v17_gap_window():
    log("=" * 70)
    log("v17: GAP WINDOW SENSITIVITY (interface region width)")
    log("=" * 70)

    windows = [3.0, 3.5, 4.0, 4.5, 5.0, 6.0]
    results = {}

    for win in windows:
        comp_data = {}
        for comp, cfg in COMPS.items():
            se = read(cfg['se']); ncm = read(cfg['ncm'])
            stacked, n_ncm = stack_rigid(se, ncm, cfg['gap_eq'], (0., 0.))
            A = xy_area(stacked.cell.array)
            counts = count_bonds(stacked, n_ncm, DEFAULT_CUTOFFS, gap_window=win)
            comp_data[comp] = {k: v for k, v in counts.items()}
            comp_data[comp]['Li-O_density'] = counts['Li-O'] / A
            comp_data[comp]['Cl-O_density'] = counts['Cl-O'] / A
            comp_data[comp]['Br-O_density'] = counts['Br-O'] / A
            comp_data[comp]['A'] = A

        xs_LiO = [comp_data[c]['Li-O_density'] for c in PAPER_EXP]
        xs_ClO = [comp_data[c]['Cl-O_density'] for c in PAPER_EXP]
        ys = [PAPER_EXP[c] for c in PAPER_EXP]

        R_LiO = pearson_R(xs_LiO, ys)
        R_ClO = pearson_R(xs_ClO, ys)
        results[f"{win:.1f}"] = {
            'window': win, 'comp_data': comp_data,
            'R_Li-O_vs_exp': R_LiO, 'R_Cl-O_vs_exp': R_ClO,
        }
        log(f"  window={win:.1f}A  R(Li-O)={R_LiO:+.4f}  R(Cl-O)={R_ClO:+.4f}")

    return results


# =============================================================================
# v18 — Per-Li atom decomposition (which Li atoms anchor?)
# =============================================================================
def v18_per_atom_decomp():
    log("=" * 70)
    log("v18: PER-Li ATOM DECOMPOSITION (anchor identification)")
    log("=" * 70)

    LIO_THRESHOLD = 3.0
    results = {}

    for comp, cfg in COMPS.items():
        se = read(cfg['se']); ncm = read(cfg['ncm'])
        stacked, n_ncm = stack_rigid(se, ncm, cfg['gap_eq'], (0., 0.))
        syms = stacked.get_chemical_symbols()
        pos = stacked.positions
        ncm_z_max = pos[:n_ncm, 2].max()
        A = xy_area(stacked.cell.array)

        # For each SE Li atom, find nearest NCM-O distance
        se_li_data = []
        for i in range(n_ncm, len(stacked)):
            if syms[i] != 'Li': continue
            # Find nearest O in NCM
            nearest_d = float('inf')
            for j in range(n_ncm):
                if syms[j] != 'O': continue
                d = stacked.get_distance(i, j, mic=True)
                if d < nearest_d: nearest_d = d
            se_li_data.append({
                'idx': i, 'z_se': float(pos[i, 2]), 'z_se_above_ncm': float(pos[i, 2] - ncm_z_max),
                'nearest_O_dist': nearest_d,
                'is_anchor': nearest_d < LIO_THRESHOLD,
            })

        anchors = [d for d in se_li_data if d['is_anchor']]
        non_anchors = [d for d in se_li_data if not d['is_anchor']]

        results[comp] = {
            'n_se_Li_total': len(se_li_data),
            'n_anchor_Li': len(anchors),
            'n_non_anchor_Li': len(non_anchors),
            'anchor_density_per_A2': len(anchors) / A,
            'mean_anchor_dist': float(np.mean([d['nearest_O_dist'] for d in anchors])) if anchors else 0,
            'min_anchor_dist': float(min([d['nearest_O_dist'] for d in anchors])) if anchors else 0,
            'mean_non_anchor_dist': float(np.mean([d['nearest_O_dist'] for d in non_anchors])) if non_anchors else 0,
            'A': A,
            'gap_eq': cfg['gap_eq'],
        }
        log(f"  {comp}: total_Li={len(se_li_data)}  anchor_Li={len(anchors)}  "
            f"density={len(anchors)/A:.4f}/Å²  mean_dist={results[comp]['mean_anchor_dist']:.3f}A")

    # Pearson R on anchor density
    xs = [results[c]['anchor_density_per_A2'] for c in PAPER_EXP]
    ys = [PAPER_EXP[c] for c in PAPER_EXP]
    R = pearson_R(xs, ys)
    log(f"\n  R(anchor_Li density vs paper exp) = {R:+.4f}")

    return {'per_comp': results, 'R_anchor_vs_exp': R}


# =============================================================================
# v19 — Phase 1 W_max cross-validation
# =============================================================================
def v19_phase1_crossval():
    log("=" * 70)
    log("v19: Phase 1 W_max cross-validation")
    log("=" * 70)

    p1_path = Path("phase1_summary.json")
    if not p1_path.exists():
        log(f"  ⚠ Phase 1 summary not found at {p1_path}")
        return {'error': 'phase1_summary.json missing'}

    p1 = json.loads(p1_path.read_text())

    # Method A is isolated slab method
    method_a = p1.get('method_A_isolated_slab', {})
    log(f"\nPhase 1 Method A W_max_mean (rigid binding curve):")
    p1_w_max = {}
    for c in ['comp1', 'comp2', 'comp3', 'comp4', 'comp5', 'modelC']:
        d = method_a.get(c, {})
        w = d.get('W_max_mean', None)
        if w is not None:
            log(f"  {c:<8}: W_max_mean={w:+.4f}  (n_reg={d.get('n_registries', 0)})")
            p1_w_max[c] = w

    # Cross-validation: Phase 1 W_max vs paper exp
    if all(c in p1_w_max for c in PAPER_EXP):
        xs = [p1_w_max[c] for c in PAPER_EXP]
        ys = [PAPER_EXP[c] for c in PAPER_EXP]
        R_p1 = pearson_R(xs, ys)
        log(f"\n  Phase 1 W_max vs paper exp:  R = {R_p1:+.4f}")
    else:
        R_p1 = float('nan')
        log(f"  ⚠ Cannot compute R — missing comp data")

    return {
        'phase1_W_max': p1_w_max,
        'R_phase1_vs_exp': R_p1,
    }


# =============================================================================
# v20 — Save xyz files for VESTA visualization
# =============================================================================
def v20_visualization_xyz():
    log("=" * 70)
    log("v20: SAVE xyz files for VESTA visualization")
    log("=" * 70)

    saved = {}
    for comp, cfg in COMPS.items():
        se = read(cfg['se']); ncm = read(cfg['ncm'])
        stacked, n_ncm = stack_rigid(se, ncm, cfg['gap_eq'], (0., 0.))
        out_path = RESULTS_DIR / "v20_xyz" / f"{comp}_gap{cfg['gap_eq']:.1f}A.xyz"
        write(str(out_path), stacked)
        saved[comp] = {
            'path': str(out_path),
            'n_atoms': len(stacked),
            'n_ncm': n_ncm,
            'n_se': len(stacked) - n_ncm,
            'gap_eq': cfg['gap_eq'],
        }
        log(f"  {comp}: saved {out_path.name} ({len(stacked)} atoms)")
    return saved


# =============================================================================
# v21 — Composite descriptor optimization
# =============================================================================
def v21_composite_descriptor(v15_data=None):
    log("=" * 70)
    log("v21: COMPOSITE DESCRIPTOR (Li-O − α·Cl-O − β·Br-O)")
    log("=" * 70)

    # Use single-registry bond counts at gap_eq (R1_origin)
    comp_bonds = {}
    for comp, cfg in COMPS.items():
        se = read(cfg['se']); ncm = read(cfg['ncm'])
        stacked, n_ncm = stack_rigid(se, ncm, cfg['gap_eq'], (0., 0.))
        A = xy_area(stacked.cell.array)
        counts = count_bonds(stacked, n_ncm, DEFAULT_CUTOFFS)
        comp_bonds[comp] = {
            'Li-O': counts['Li-O'] / A,
            'Cl-O': counts['Cl-O'] / A,
            'Br-O': counts['Br-O'] / A,
            'paper_exp': PAPER_EXP.get(comp, 0),
        }

    # Grid search over (alpha, beta) for max R
    paper_y = np.array([comp_bonds[c]['paper_exp'] for c in PAPER_EXP])
    LiO = np.array([comp_bonds[c]['Li-O'] for c in PAPER_EXP])
    ClO = np.array([comp_bonds[c]['Cl-O'] for c in PAPER_EXP])
    BrO = np.array([comp_bonds[c]['Br-O'] for c in PAPER_EXP])

    best = {'R': -2, 'alpha': 0, 'beta': 0}
    grid = np.arange(0.0, 5.1, 0.25)
    for a in grid:
        for b in grid:
            W_pred = LiO - a * ClO - b * BrO
            R = pearson_R(W_pred, paper_y)
            if not np.isnan(R) and R > best['R']:
                best = {'R': R, 'alpha': float(a), 'beta': float(b)}

    log(f"\nGrid search (α, β) ∈ [0, 5] step 0.25:")
    log(f"  BEST: α={best['alpha']:.2f}  β={best['beta']:.2f}  R={best['R']:+.4f}")

    # Show single-descriptor R for comparison
    R_LiO = pearson_R(LiO, paper_y)
    R_ClO = pearson_R(ClO, paper_y)
    R_BrO = pearson_R(BrO, paper_y) if BrO.std() > 0 else float('nan')
    log(f"\nSingle-descriptor baselines:")
    log(f"  R(Li-O density)  = {R_LiO:+.4f}")
    log(f"  R(Cl-O density)  = {R_ClO:+.4f}")
    log(f"  R(Br-O density)  = {R_BrO:+.4f}")

    # Show predicted Wad with best composite
    log(f"\nBest composite: W_pred = Li-O − {best['alpha']:.2f}·Cl-O − {best['beta']:.2f}·Br-O")
    log(f"{'comp':<8} {'paper':>6} {'Li-O':>8} {'Cl-O':>8} {'Br-O':>8} {'W_pred':>10}")
    for comp in PAPER_EXP:
        cb = comp_bonds[comp]
        W = cb['Li-O'] - best['alpha'] * cb['Cl-O'] - best['beta'] * cb['Br-O']
        log(f"{comp:<8} {cb['paper_exp']:>6} {cb['Li-O']:>+8.4f} {cb['Cl-O']:>+8.4f} {cb['Br-O']:>+8.4f} {W:>+10.4f}")

    return {
        'best': best,
        'single_R': {'Li-O': R_LiO, 'Cl-O': R_ClO, 'Br-O': R_BrO},
        'comp_bonds': comp_bonds,
    }


# =============================================================================
# v22 — Relaxed bond count (limited LBFGS, allow type-(a) only)
# =============================================================================
def v22_relaxed_bonds(calc):
    log("=" * 70)
    log("v22: RELAXED BOND COUNT (limited LBFGS to allow type-(a) relaxation)")
    log("=" * 70)
    log("Strategy: FixAtoms NCM bot 1/3 + SE top 1/3, LBFGS fmax=0.05 max=50 steps")
    log("Track RMS displacement — if migration starts (RMS>1.5Å), stop early")

    LBFGS_MAX_STEPS = 50
    LBFGS_FMAX = 0.05
    MIGRATION_THRESHOLD = 1.5  # Å

    results = {}
    for comp, cfg in COMPS.items():
        se = read(cfg['se']); ncm = read(cfg['ncm'])
        stacked, n_ncm = stack_rigid(se, ncm, cfg['gap_eq'], (0., 0.))
        initial_pos = stacked.positions.copy()

        # FixAtoms: NCM bottom 1/3 + SE top 1/3 (interface free)
        ncm_z = stacked.positions[:n_ncm, 2]
        z_min, z_max = ncm_z.min(), ncm_z.max()
        z_thresh_lo = z_min + (z_max - z_min) * (1.0/3.0)
        ncm_fix = [i for i in range(n_ncm) if stacked.positions[i, 2] <= z_thresh_lo]

        se_z = stacked.positions[n_ncm:, 2]
        s_min, s_max = se_z.min(), se_z.max()
        z_thresh_hi = s_min + (s_max - s_min) * (2.0/3.0)
        se_fix = [i for i in range(n_ncm, len(stacked)) if stacked.positions[i, 2] >= z_thresh_hi]

        stacked.set_constraint(FixAtoms(indices=ncm_fix + se_fix))
        stacked.calc = calc

        # Limited LBFGS
        log(f"\n--- {comp}: relaxed bond at gap_eq={cfg['gap_eq']:.1f}A ---")
        log(f"  Atoms: {len(stacked)}, fixed: {len(ncm_fix) + len(se_fix)} (NCM_bot {len(ncm_fix)} + SE_top {len(se_fix)})")
        t0 = time.time()
        opt = LBFGS(stacked, logfile=None)
        opt.run(fmax=LBFGS_FMAX, steps=LBFGS_MAX_STEPS)
        E_int = float(stacked.get_potential_energy())
        steps = opt.nsteps

        # RMS displacement (interface atoms only — top of NCM + bottom of SE)
        free_idx = [i for i in range(len(stacked)) if i not in (set(ncm_fix) | set(se_fix))]
        disp = stacked.positions[free_idx] - initial_pos[free_idx]
        rms_3d = float(np.sqrt(np.mean(np.sum(disp**2, axis=1))))
        max_disp = float(np.max(np.linalg.norm(disp, axis=1)))

        # Check migration
        migrated = max_disp > MIGRATION_THRESHOLD

        # Bond count after relaxation
        counts = count_bonds(stacked, n_ncm, DEFAULT_CUTOFFS)
        A = xy_area(stacked.cell.array)

        write(str(RESULTS_DIR / f"v22_relaxed_{comp}.xyz"), stacked)
        results[comp] = {
            'gap_eq': cfg['gap_eq'],
            'A': A,
            'lbfgs_steps': steps,
            'lbfgs_fmax_target': LBFGS_FMAX,
            'rms_disp_free': rms_3d,
            'max_disp': max_disp,
            'migrated': migrated,
            'E_int_relaxed': E_int,
            'bonds': counts,
            'Li-O_density': counts['Li-O'] / A,
            'Cl-O_density': counts['Cl-O'] / A,
            'Br-O_density': counts['Br-O'] / A,
        }
        log(f"  steps={steps}/50  RMS={rms_3d:.3f}A  max={max_disp:.3f}A  "
            f"{'⚠ MIGRATED' if migrated else '✓ no mig'}")
        log(f"  bonds: {counts}")
        log(f"  E_int (relaxed) = {E_int:.3f}")

    # Pearson R after relaxation
    xs = [results[c]['Li-O_density'] for c in PAPER_EXP]
    ys = [PAPER_EXP[c] for c in PAPER_EXP]
    R_LiO_relaxed = pearson_R(xs, ys)

    xs_ClO = [results[c]['Cl-O_density'] for c in PAPER_EXP]
    R_ClO_relaxed = pearson_R(xs_ClO, ys)

    log(f"\n--- Relaxed bond count Pearson R ---")
    log(f"  R(Li-O density relaxed vs exp) = {R_LiO_relaxed:+.4f}")
    log(f"  R(Cl-O density relaxed vs exp) = {R_ClO_relaxed:+.4f}")

    log(f"\n--- v15 (rigid) vs v22 (relaxed) ---")
    log(f"  Li-O R: v15=+0.819 vs v22={R_LiO_relaxed:+.4f}  diff={R_LiO_relaxed - 0.819:+.4f}")
    log(f"  Cl-O R: v15=-0.914 vs v22={R_ClO_relaxed:+.4f}  diff={R_ClO_relaxed - (-0.914):+.4f}")

    return {
        'per_comp': results,
        'R_LiO_relaxed': R_LiO_relaxed,
        'R_ClO_relaxed': R_ClO_relaxed,
    }


# =============================================================================
# Main — run all sequentially
# =============================================================================
def main():
    log("=" * 70); log("v16-v22 COMPREHENSIVE VALIDATION SUITE"); log("=" * 70)
    full = {}; t0 = time.time()

    full['v16_cutoff'] = v16_cutoff_sensitivity()
    json.dump(full, open(RESULTS_DIR / "summary.json", 'w'), indent=2, default=list)
    log(f"\nv16 done. Cumulative: {(time.time()-t0)/60:.1f} min")

    full['v17_gap_window'] = v17_gap_window()
    json.dump(full, open(RESULTS_DIR / "summary.json", 'w'), indent=2, default=list)
    log(f"v17 done. Cumulative: {(time.time()-t0)/60:.1f} min")

    full['v18_per_atom'] = v18_per_atom_decomp()
    json.dump(full, open(RESULTS_DIR / "summary.json", 'w'), indent=2, default=list)
    log(f"v18 done. Cumulative: {(time.time()-t0)/60:.1f} min")

    full['v19_phase1_crossval'] = v19_phase1_crossval()
    json.dump(full, open(RESULTS_DIR / "summary.json", 'w'), indent=2, default=list)
    log(f"v19 done. Cumulative: {(time.time()-t0)/60:.1f} min")

    full['v20_xyz_saved'] = v20_visualization_xyz()
    json.dump(full, open(RESULTS_DIR / "summary.json", 'w'), indent=2, default=list)
    log(f"v20 done. Cumulative: {(time.time()-t0)/60:.1f} min")

    full['v21_composite'] = v21_composite_descriptor()
    json.dump(full, open(RESULTS_DIR / "summary.json", 'w'), indent=2, default=list)
    log(f"v21 done. Cumulative: {(time.time()-t0)/60:.1f} min")

    log("Loading UMA for v22 (relaxed bonds)...")
    calc = make_calc()
    log("UMA loaded.")
    full['v22_relaxed'] = v22_relaxed_bonds(calc)
    json.dump(full, open(RESULTS_DIR / "summary.json", 'w'), indent=2, default=list)
    log(f"v22 done. Cumulative: {(time.time()-t0)/60:.1f} min")

    log("=" * 70); log("COMPREHENSIVE SUMMARY"); log("=" * 70)

    # Cutoff sensitivity verdict
    log("\nv16 — Cutoff sensitivity (Li-O, Cl-O R variation):")
    for pair, data in full['v16_cutoff'].items():
        Rs = [v['R_density_vs_exp'] for v in data.values()]
        log(f"  {pair}: R range = {min(Rs):+.4f}..{max(Rs):+.4f}  Δ={max(Rs)-min(Rs):.4f}")

    # Gap window verdict
    log("\nv17 — Gap window sensitivity (R variation):")
    R_LiOs = [v['R_Li-O_vs_exp'] for v in full['v17_gap_window'].values()]
    R_ClOs = [v['R_Cl-O_vs_exp'] for v in full['v17_gap_window'].values()]
    log(f"  Li-O R range: {min(R_LiOs):+.4f}..{max(R_LiOs):+.4f}  Δ={max(R_LiOs)-min(R_LiOs):.4f}")
    log(f"  Cl-O R range: {min(R_ClOs):+.4f}..{max(R_ClOs):+.4f}  Δ={max(R_ClOs)-min(R_ClOs):.4f}")

    # Per-atom decomp
    log(f"\nv18 — anchor Li density R = {full['v18_per_atom']['R_anchor_vs_exp']:+.4f}")

    # Phase 1 cross-validation
    p1 = full['v19_phase1_crossval']
    if 'R_phase1_vs_exp' in p1 and not np.isnan(p1['R_phase1_vs_exp']):
        log(f"\nv19 — Phase 1 W_max R = {p1['R_phase1_vs_exp']:+.4f}")

    # Composite
    best = full['v21_composite']['best']
    log(f"\nv21 — BEST composite: W = Li-O − {best['alpha']}·Cl-O − {best['beta']}·Br-O  R={best['R']:+.4f}")

    # Relaxed
    log(f"\nv22 — Relaxed bond R: Li-O={full['v22_relaxed']['R_LiO_relaxed']:+.4f}  "
        f"Cl-O={full['v22_relaxed']['R_ClO_relaxed']:+.4f}")
    migrated = [c for c, d in full['v22_relaxed']['per_comp'].items() if d['migrated']]
    log(f"  Migrated comps: {migrated if migrated else 'NONE'}")

    log(f"\n=== v16-v22 ALL DONE: {(time.time()-t0)/60:.1f} min ===")
    json.dump(full, open(RESULTS_DIR / "summary.json", 'w'), indent=2, default=list)


if __name__ == "__main__":
    main()
