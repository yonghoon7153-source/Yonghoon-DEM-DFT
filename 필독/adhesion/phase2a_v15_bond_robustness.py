"""Phase 2a v15 — bond count REGISTRY ROBUSTNESS check.

User concern: v14 bond counts were at single registry (R1_origin).
- comp1 Cl-O = 8 might be artifact of THIS specific xy-shift
- Different shift might give Cl-O = 0 or Cl-O = 20
- Pattern (Li6 Cl-O > 0, Li5.4 Cl-O = 0) might be GEOMETRY artifact

v15 tests: count bonds at 36 xy-shifts per comp at gap_eq.
- mean ± std → robustness measure
- Cross-comp ranking at MEAN values → true pattern
- If std large → artifact, NOT robust signal

Inputs (from v14 Phase B):
  comp1: gap_eq=1.2, comp2: gap_eq=1.2, comp3: gap_eq=1.4
  comp4: gap_eq=1.6, comp5: gap_eq=1.6, modelC: gap_eq=1.2

Pure geometry (no UMA, no energy). Time: ~30 sec total.
"""
import os, json, time
from pathlib import Path
import numpy as np
from ase.io import read, write

COMPS = {
    'comp1':  {'se': 'comp1_slab_v2.xyz',            'ncm': 'ncm_7x7x1_3Lconv.xyz', 'gap_eq': 1.2},
    'comp2':  {'se': 'comp2_slab_v2.xyz',            'ncm': 'ncm_7x7x1_3Lconv.xyz', 'gap_eq': 1.2},
    'comp3':  {'se': 'comp3_slab_v1_PRESERVED.xyz',  'ncm': 'ncm_5x5x1_3Lconv.xyz', 'gap_eq': 1.4},
    'comp4':  {'se': 'comp4_slab_v1_PRESERVED.xyz',  'ncm': 'ncm_5x5x1_3Lconv.xyz', 'gap_eq': 1.6},
    'comp5':  {'se': 'comp5_slab_v1_PRESERVED.xyz',  'ncm': 'ncm_5x5x1_3Lconv.xyz', 'gap_eq': 1.6},
    'modelC': {'se': 'modelC_slab_v2_PRESERVED.xyz', 'ncm': 'ncm_5x5x1_3Lconv.xyz', 'gap_eq': 1.2},
}

HIGH_SYM = [
    ("R1_origin", (0.0, 0.0)), ("R2_half_x", (0.5, 0.0)),
    ("R3_half_y", (0.0, 0.5)), ("R4_diagonal", (0.5, 0.5)),
    ("R5_hex1", (1/3, 2/3)),   ("R6_hex2", (2/3, 1/3)),
]
N_RANDOM = 30
RANDOM_SEED = 42

BOND_CUTOFFS = {
    ('Li', 'O'): 3.0, ('Cl', 'O'): 3.5, ('Br', 'O'): 3.7,
    ('S', 'Li'): 3.0, ('S', 'Ni'): 3.5, ('Li', 'Ni'): 3.5,
}
VACUUM_TOP = 30.0
PAPER_EXP = {'comp1': 194, 'comp2': 180, 'comp3': 316, 'comp4': 298, 'comp5': 249}

RESULTS_DIR = Path("phase2a_v15_results"); RESULTS_DIR.mkdir(exist_ok=True)
LOG_FILE = RESULTS_DIR / "progress.log"


def log(msg):
    s = f"[{time.strftime('%H:%M:%S')}] {msg}"
    print(s, flush=True)
    with open(LOG_FILE, 'a') as f:
        f.write(s + "\n")


def stack_rigid(se, ncm, gap, shift_frac):
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


def main():
    log("=" * 70)
    log("v15 — bond count REGISTRY ROBUSTNESS check (36 shifts/comp)")
    log("=" * 70)

    rng = np.random.default_rng(RANDOM_SEED)
    RANDOM_REG = [(f"rand_{i+1:03d}", (rng.uniform(0, 1), rng.uniform(0, 1)))
                  for i in range(N_RANDOM)]
    ALL_REG = HIGH_SYM + RANDOM_REG
    log(f"Total registries per comp: {len(ALL_REG)}")
    log(f"Bond cutoffs: {BOND_CUTOFFS}")

    full_results = {}
    t_start = time.time()

    for comp, cfg in COMPS.items():
        gap_eq = cfg['gap_eq']
        se = read(cfg['se'])
        ncm = read(cfg['ncm'])
        log(f"\n--- {comp}: 36 registries at gap_eq={gap_eq:.1f} Å ---")

        bond_per_reg = {k: [] for k in [f"{a}-{b}" for a, b in BOND_CUTOFFS]}
        densities_per_reg = {k: [] for k in bond_per_reg}
        A_first = None

        for name, shift in ALL_REG:
            stacked, n_ncm = stack_rigid(se, ncm, gap_eq, shift)
            counts = count_interface_bonds(stacked, n_ncm)
            A = xy_area(stacked.cell.array)
            if A_first is None:
                A_first = A
            for k, v in counts.items():
                bond_per_reg[k].append(v)
                densities_per_reg[k].append(v / A)

        # Statistics
        stats = {}
        for k in bond_per_reg:
            vals = bond_per_reg[k]
            dens = densities_per_reg[k]
            stats[k] = {
                'mean': float(np.mean(vals)),
                'std': float(np.std(vals)),
                'min': int(np.min(vals)),
                'max': int(np.max(vals)),
                'range': int(np.max(vals) - np.min(vals)),
                'cv_pct': float(100 * np.std(vals) / np.mean(vals)) if np.mean(vals) > 0 else 0,
                'mean_density': float(np.mean(dens)),
                'std_density': float(np.std(dens)),
            }
            log(f"  {comp} {k:<10s}: mean={stats[k]['mean']:>5.1f}  std={stats[k]['std']:>4.1f}  "
                f"range={stats[k]['min']}-{stats[k]['max']}  CV={stats[k]['cv_pct']:>4.1f}%")
        full_results[comp] = {'gap_eq': gap_eq, 'A': A_first, 'stats': stats,
                              'bond_per_reg': bond_per_reg, 'densities_per_reg': densities_per_reg}

    # Cross-comp ranking analysis
    log("\n" + "=" * 70)
    log("CROSS-COMP RANKING ROBUSTNESS")
    log("=" * 70)

    # Mean bond density per comp
    log(f"\n{'comp':<8} {'paper':>6} {'gap_eq':>8} {'<Li-O/Å²>':>11} {'<Cl-O/Å²>':>11} {'<Br-O/Å²>':>11}")
    for comp in ['comp1', 'comp2', 'comp3', 'comp4', 'comp5', 'modelC']:
        s = full_results[comp]['stats']
        paper = PAPER_EXP.get(comp, 0)
        log(f"{comp:<8} {paper:>6} {full_results[comp]['gap_eq']:>8.1f} "
            f"{s['Li-O']['mean_density']:>+11.4f} {s['Cl-O']['mean_density']:>+11.4f} "
            f"{s['Br-O']['mean_density']:>+11.4f}")

    log(f"\n{'comp':<8} {'Li-O range':>15} {'Cl-O range':>15} {'Br-O range':>15}")
    for comp in ['comp1', 'comp2', 'comp3', 'comp4', 'comp5', 'modelC']:
        s = full_results[comp]['stats']
        log(f"{comp:<8} "
            f"{s['Li-O']['min']:>3}..{s['Li-O']['max']:>3} (CV={s['Li-O']['cv_pct']:.0f}%)   "
            f"{s['Cl-O']['min']:>3}..{s['Cl-O']['max']:>3} (CV={s['Cl-O']['cv_pct']:.0f}%)   "
            f"{s['Br-O']['min']:>3}..{s['Br-O']['max']:>3} (CV={s['Br-O']['cv_pct']:.0f}%)")

    # Pearson R using MEAN values
    log(f"\n--- Pearson R using MEAN bond densities (n=5 paper comps) ---")
    table = []
    for comp in ['comp1', 'comp2', 'comp3', 'comp4', 'comp5']:
        s = full_results[comp]['stats']
        table.append({
            'comp': comp,
            'paper': PAPER_EXP[comp],
            'Li-O_density_mean': s['Li-O']['mean_density'],
            'Cl-O_density_mean': s['Cl-O']['mean_density'],
            'Br-O_density_mean': s['Br-O']['mean_density'],
            'Li-O_count_mean': s['Li-O']['mean'],
            'Cl-O_count_mean': s['Cl-O']['mean'],
            'Br-O_count_mean': s['Br-O']['mean'],
        })

    paper_y = np.array([r['paper'] for r in table])
    pearsons = {}
    for d in ['Li-O_density_mean', 'Cl-O_density_mean', 'Br-O_density_mean',
              'Li-O_count_mean', 'Cl-O_count_mean', 'Br-O_count_mean']:
        x = np.array([r[d] for r in table])
        if x.std() == 0:
            pearsons[d] = float('nan')
            log(f"  R({d:<22}) = nan")
            continue
        r = float(np.corrcoef(x, paper_y)[0, 1])
        pearsons[d] = r
        flag = "⭐" if abs(r) > 0.9 else "+" if abs(r) > 0.7 else " "
        log(f"  R({d:<22}) = {r:+.4f}  {flag}")

    # Compare with v14 single-registry result
    log(f"\n--- Compare v14 (single R1_origin) vs v15 (mean of 36 reg) ---")
    log(f"{'descriptor':<25} {'v14 (R1)':>12} {'v15 (mean)':>12} {'consistent?':>15}")
    v14_pearson = {
        'Li-O_density_mean': +0.8325,   # was +0.83 in v14
        'Cl-O_density_mean': -0.9131,    # was -0.91 in v14
        'Br-O_density_mean': +0.4028,    # was +0.40
    }
    for d in ['Li-O_density_mean', 'Cl-O_density_mean', 'Br-O_density_mean']:
        old = v14_pearson.get(d, 0)
        new = pearsons.get(d, 0)
        sign_same = "✓" if (old * new > 0) else "✗"
        magnitude_close = "✓" if abs(old - new) < 0.15 else "✗ shifted"
        log(f"  {d:<25} {old:>+12.4f} {new:>+12.4f}    sign:{sign_same} mag:{magnitude_close}")

    # Verdict
    log(f"\n--- VERDICT ---")
    log(f"If CV (std/mean) of bond counts is LARGE (>30%): registry-dependent ARTIFACT")
    log(f"If CV SMALL (<10%): bond count is robust intrinsic feature")

    cvs = []
    for comp in ['comp1', 'comp2', 'comp3', 'comp4', 'comp5']:
        for k in ['Li-O', 'Cl-O', 'Br-O']:
            cv = full_results[comp]['stats'][k]['cv_pct']
            if cv > 0:
                cvs.append((comp, k, cv))
    if cvs:
        avg_cv = np.mean([c[2] for c in cvs])
        max_cv = max(cvs, key=lambda x: x[2])
        log(f"  Average CV (excluding 0-bond cases): {avg_cv:.1f}%")
        log(f"  Max CV: {max_cv[0]} {max_cv[1]} = {max_cv[2]:.1f}%")
        if avg_cv < 15:
            log(f"  ✓ Bond count ROBUST across registries (avg CV < 15%)")
        elif avg_cv < 30:
            log(f"  △ Moderate variation, mean values still meaningful")
        else:
            log(f"  ✗ HIGH variation — bond count is REGISTRY ARTIFACT")

    log(f"\n=== v15 DONE: {(time.time()-t_start)/60:.1f} min ===")
    json.dump(full_results, open(RESULTS_DIR / "results.json", 'w'), indent=2, default=list)
    json.dump({'pearson_R_mean_density': pearsons, 'v14_vs_v15': True},
              open(RESULTS_DIR / "pearson_summary.json", 'w'), indent=2)


if __name__ == "__main__":
    main()
