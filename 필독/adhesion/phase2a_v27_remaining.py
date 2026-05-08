"""Phase 2a v27 — REMAINING EXTRAS (A, D, E, F, G, H from candidate list).

User direction: "할 수 있는 거 다 해보자". This script covers all candidate
items except C (MACE install — separate) and B (DFT — excluded).

Phases:
  A  Phase 1 cross-validation: load db/adhesion.json phase1_rigid_binding
     W_max per comp, compute R vs paper exp, compare with v15 Cl-O R
  D  Halogen z-distribution gaussian fit per comp:
     fit Cl, Br z-positions to Gaussian, get mean and std,
     correlate "z-mean position" and "spread" with paper exp
  E  Bond density bootstrap CI:
     resample n=5 paper comps with replacement (1000 iter),
     compute R(Cl-O), R(Li-O) distribution, get 95% CI
  F  Cij vs adhesion R comparison:
     load db/elastic.json mlip_300K_supercell, compute R between
     each Cij component (B, K, G, E, nu, C11, C44) and paper exp,
     compare with R(Cl-O) descriptor
  G  Larger NCM cell convergence:
     build 7x7x5 NCM (vs current 7x7x1 / 5x5x1), recount bonds,
     check if R(Cl-O) and density values converge
  H  1000 xy-shift registries (vs v15's 36):
     re-do v15 with 1000 random registries, refine CV measurement
     for each comp's Cl-O density

Inputs: db/adhesion.json, db/elastic.json (downloaded), SE/NCM xyz on KISTI
Time: ~30-45 min on KISTI (G, H expensive; A, D, E, F < 2 min total)
"""
import os, json, time, sys, traceback, urllib.request
from pathlib import Path
import numpy as np
from ase import Atoms
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
V15 = {'R_Li-O': +0.8175, 'R_Cl-O': -0.9136, 'R_Br-O': +0.4028}

DB_BASE = "https://raw.githubusercontent.com/yonghoon7153-source/Yonghoon-DEM-DFT/claude/review-ml-migration-W29af/db/properties"

RESULTS_DIR = Path("phase2a_v27_results"); RESULTS_DIR.mkdir(exist_ok=True)
LOG_FILE = RESULTS_DIR / "run.log"


def log(msg):
    s = f"[{time.strftime('%H:%M:%S')}] {msg}"
    print(s, flush=True)
    with open(LOG_FILE, 'a') as f:
        f.write(s + "\n")


def fetch_db_json(name):
    """Fetch JSON from GitHub if not local."""
    if Path(name).exists():
        return json.load(open(name))
    url = f"{DB_BASE}/{name}"
    log(f"  fetching {name} from GitHub...")
    return json.load(urllib.request.urlopen(url, timeout=15))


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


# =====================================================================
# A — Phase 1 W_max cross-validation
# =====================================================================

def phase_A_phase1_crossval():
    log("\n" + "=" * 70)
    log("A: Phase 1 W_max cross-validation (independent method)")
    log("=" * 70)
    out = {}
    try:
        adhesion = fetch_db_json("adhesion.json")
        p1 = adhesion['phase1_rigid_binding_2026_05_06']
    except Exception as e:
        log(f"  cannot load Phase 1 data: {e}")
        return {'error': str(e)}

    for method_label, method_key in [('Method_A_isolated', 'method_A_isolated_slab'),
                                       ('Method_B_self_ref', 'method_B_self_reference')]:
        m = p1.get(method_key, {})
        results = m.get('results', {})
        if not results:
            log(f"  {method_label}: no results")
            continue
        wmax = {c: results.get(c, {}).get('W_max_J_per_m2') for c in PAPER_COMPS}
        if any(v is None for v in wmax.values()):
            log(f"  {method_label}: incomplete data")
            continue
        log(f"\n--- {method_label}: W_max (J/m²) per comp ---")
        log(f"{'comp':<8} {'paper':>6} {'W_max':>8} {'std':>8} {'d_min':>8}")
        for c in PAPER_COMPS:
            r = results[c]
            log(f"{c:<8} {PAPER_EXP[c]:>6} {r.get('W_max_J_per_m2',0):>+8.3f} "
                f"{r.get('W_max_std',0):>8.3f} {r.get('d_min_A',0):>8.3f}")
        x = [wmax[c] for c in PAPER_COMPS]
        y = [PAPER_EXP[c] for c in PAPER_COMPS]
        R = pearson(x, y)
        log(f"  R(W_max vs paper) = {R:+.4f}")
        log(f"  Compare v15 R(Cl-O) = {V15['R_Cl-O']:+.4f}")
        if R * V15['R_Cl-O'] > 0:
            log(f"  ✓ Same sign as Cl-O density: independent confirmation")
        else:
            log(f"  ✗ Opposite sign — methods disagree")
        out[method_label] = {'wmax': wmax, 'R': R}
    return out


# =====================================================================
# D — Halogen z-distribution gaussian fit
# =====================================================================

def phase_D_halogen_zfit():
    log("\n" + "=" * 70)
    log("D: Halogen z-distribution gaussian fit per comp")
    log("=" * 70)
    out = {}
    log(f"\n{'comp':<8} {'X':>3} {'mean(z_norm)':>13} {'std(z_norm)':>12} "
        f"{'skew':>8} {'top20%':>8} {'bot20%':>8}")
    for c in ALL_COMPS:
        try:
            se = read(COMPS[c]['se'])
            z = se.positions[:, 2]
            z_min, z_max = z.min(), z.max()
            z_norm = (z - z_min) / (z_max - z_min)  # 0..1
            syms = se.get_chemical_symbols()
            for X in ['Cl', 'Br']:
                idxs = [i for i, s in enumerate(syms) if s == X]
                if not idxs:
                    continue
                zs = z_norm[idxs]
                mean = float(np.mean(zs))
                std = float(np.std(zs))
                # third moment / std^3 = skewness
                if std > 0:
                    skew = float(np.mean(((zs - mean)/std)**3))
                else:
                    skew = 0.0
                top20 = float(np.mean(zs > 0.8))
                bot20 = float(np.mean(zs < 0.2))
                log(f"{c:<8} {X:>3} {mean:>+13.4f} {std:>12.4f} {skew:>+8.3f} "
                    f"{top20:>8.2f} {bot20:>8.2f}")
                out.setdefault(c, {})[X] = {
                    'mean': mean, 'std': std, 'skew': skew,
                    'top20_frac': top20, 'bot20_frac': bot20,
                }
        except Exception as e:
            log(f"  {c} FAILED: {e}")

    # Correlations vs paper exp
    log(f"\n--- Pearson R vs paper exp (n=5 comps) ---")
    for X in ['Cl', 'Br']:
        for metric in ['mean', 'std', 'skew', 'top20_frac', 'bot20_frac']:
            xs, ys = [], []
            for c in PAPER_COMPS:
                d = out.get(c, {}).get(X)
                if d:
                    xs.append(d[metric]); ys.append(PAPER_EXP[c])
            if len(xs) < 5:
                continue
            R = pearson(xs, ys)
            flag = "⭐" if abs(R) > 0.85 else ("+" if abs(R) > 0.7 else "")
            log(f"  R({X} {metric:<14}) = {R:+.4f}  {flag}")
    return out


# =====================================================================
# E — Bond density bootstrap CI (resample n=5)
# =====================================================================

def phase_E_bootstrap_R():
    log("\n" + "=" * 70)
    log("E: Bond density bootstrap CI for R (n=5, 1000 iter)")
    log("=" * 70)

    # Compute densities per comp at gap_eq (no shift, R1_origin)
    densities = {}
    for c in ALL_COMPS:
        try:
            se = read(COMPS[c]['se'])
            ncm = read(COMPS[c]['ncm'])
            stacked, n_ncm = stack_rigid(se, ncm, COMPS[c]['gap_eq'])
            counts = count_interface_bonds(stacked, n_ncm)
            A = xy_area(stacked.cell.array)
            densities[c] = {k: v / A for k, v in counts.items()}
        except Exception as e:
            log(f"  {c} FAILED: {e}")

    paper = np.array([PAPER_EXP[c] for c in PAPER_COMPS], float)
    rng = np.random.default_rng(42)
    N_BOOT = 1000

    log(f"\n{'bond':<8} {'R_point':>10} {'R_mean':>10} {'R_std':>10} "
        f"{'CI95_low':>10} {'CI95_high':>10}")
    for bond in ['Li-O', 'Cl-O', 'Br-O', 'S-Li', 'S-Ni', 'Li-Ni']:
        x = np.array([densities[c].get(bond, 0) for c in PAPER_COMPS], float)
        if x.std() == 0:
            continue
        R_point = pearson(x, paper)
        Rs = []
        for _ in range(N_BOOT):
            idx = rng.integers(0, 5, 5)
            xb = x[idx]; yb = paper[idx]
            if xb.std() == 0 or yb.std() == 0:
                continue
            Rs.append(pearson(xb, yb))
        Rs = np.array(Rs)
        log(f"{bond:<8} {R_point:>+10.4f} {Rs.mean():>+10.4f} {Rs.std():>10.4f} "
            f"{np.percentile(Rs, 2.5):>+10.4f} {np.percentile(Rs, 97.5):>+10.4f}")
    return {'densities': densities, 'N_BOOT': N_BOOT}


# =====================================================================
# F — Cij vs adhesion R comparison
# =====================================================================

def phase_F_cij_vs_adhesion():
    log("\n" + "=" * 70)
    log("F: Cij vs adhesion R comparison")
    log("=" * 70)
    try:
        elastic = fetch_db_json("elastic.json")
    except Exception as e:
        log(f"  cannot load elastic: {e}")
        return {'error': str(e)}

    # Try mlip_300K_supercell first
    sec = elastic.get('mlip_300K_supercell_2x2x1', {}).get('results', [])
    if not sec:
        sec = elastic.get('mlip_600K_snapshot', {}).get('results', [])
    if not sec or not isinstance(sec, list):
        log("  no comp-level Cij found")
        return {'error': 'no Cij'}

    by_comp = {row['id']: row for row in sec if 'id' in row}
    log(f"\n--- Cij per comp (source: mlip_300K_supercell_2x2x1) ---")
    fields = ['C11', 'C12', 'C44', 'K', 'G', 'E', 'nu']
    log(f"{'comp':<8} " + ' '.join(f"{f:>7}" for f in fields))
    for c in PAPER_COMPS:
        row = by_comp.get(c, {})
        log(f"{c:<8} " + ' '.join(f"{row.get(f, 0):>7.2f}" for f in fields))

    log(f"\n--- Pearson R(Cij vs paper exp Wad), v15 R(Cl-O)={V15['R_Cl-O']:+.4f} ---")
    paper = [PAPER_EXP[c] for c in PAPER_COMPS]
    for f in fields:
        x = [by_comp.get(c, {}).get(f) for c in PAPER_COMPS]
        if None in x or any(v is None for v in x):
            continue
        R = pearson(x, paper)
        flag = "⭐" if abs(R) > 0.85 else ("+" if abs(R) > 0.7 else "")
        log(f"  R({f:<4}) = {R:+.4f}  {flag}")
    return {'by_comp': by_comp}


# =====================================================================
# G — Larger NCM (5-layer 7x7x5) convergence
# =====================================================================

def phase_G_larger_ncm():
    log("\n" + "=" * 70)
    log("G: Larger NCM (5-layer build) convergence")
    log("=" * 70)
    log("  Build LiNiO2 5-layer slab via ase.spacegroup.crystal + surface,")
    log("  stack with each comp's SE, recount bonds. Compare with v15 baseline.")
    try:
        from ase.spacegroup import crystal
        from ase.build import surface
    except ImportError as e:
        log(f"  ase build unavailable: {e}")
        return {'error': str(e)}

    a, c_lat = 2.879, 14.176
    linio2 = crystal(['Li', 'Ni', 'O'],
                     basis=[(0, 0, 0), (0, 0, 0.5), (0, 0, 0.258)],
                     spacegroup=166,
                     cellpar=[a, a, c_lat, 90, 90, 120])
    # 5-layer (104) facet, supercell xy
    ncm5 = surface(linio2, (1, 0, 4), 5, vacuum=0.0)
    ncm5 = ncm5.repeat((5, 5, 1))
    ncm5.center(vacuum=0.0, axis=2)
    log(f"  Built NCM (104) 5L: {len(ncm5)} atoms, "
        f"cell xy={ncm5.cell.array[0][:2].round(2)} {ncm5.cell.array[1][:2].round(2)}")

    densities = {}
    for c in ALL_COMPS:
        try:
            se = read(COMPS[c]['se'])
            stacked, n_ncm = stack_rigid(se, ncm5, COMPS[c]['gap_eq'])
            counts = count_interface_bonds(stacked, n_ncm)
            A = xy_area(stacked.cell.array)
            densities[c] = {k: v / A for k, v in counts.items()}
        except Exception as e:
            log(f"  {c} FAILED: {e}")

    log(f"\n--- G (NCM 5L 104): bond densities ---")
    log(f"{'comp':<8} {'paper':>6} {'Li-O':>10} {'Cl-O':>10} {'Br-O':>10}")
    for c in ALL_COMPS:
        d = densities.get(c, {})
        log(f"{c:<8} {PAPER_EXP.get(c, 0):>6} "
            f"{d.get('Li-O',0):>+10.4f} {d.get('Cl-O',0):>+10.4f} {d.get('Br-O',0):>+10.4f}")

    paper = [PAPER_EXP[c] for c in PAPER_COMPS]
    R_results = {}
    for bond in ['Li-O', 'Cl-O', 'Br-O']:
        xs = [densities.get(c, {}).get(bond, 0) for c in PAPER_COMPS]
        R = pearson(xs, paper)
        delta = R - V15[f'R_{bond}']
        flag = "OK" if abs(delta) < 0.15 else "DIFF"
        log(f"  R({bond}) = {R:+.4f}  (v15: {V15[f'R_{bond}']:+.4f}, d={delta:+.3f}, {flag})")
        R_results[bond] = R
    return {'R': R_results, 'densities': densities, 'n_ncm5': len(ncm5)}


# =====================================================================
# H — 1000 xy-shift registries
# =====================================================================

def phase_H_1000_reg():
    log("\n" + "=" * 70)
    log("H: 1000 xy-shift registries (refined CV measurement)")
    log("=" * 70)
    N = 1000
    rng = np.random.default_rng(42)
    shifts = [(rng.uniform(0, 1), rng.uniform(0, 1)) for _ in range(N)]

    summary = {}
    paper = np.array([PAPER_EXP[c] for c in PAPER_COMPS], float)

    for c in ALL_COMPS:
        try:
            se = read(COMPS[c]['se'])
            ncm = read(COMPS[c]['ncm'])
            log(f"\n--- {c}: 1000 reg at gap_eq={COMPS[c]['gap_eq']:.1f} A ---")
            t0 = time.time()
            bonds_all = {f"{a}-{b}": [] for (a, b) in BOND_CUTOFFS}
            for shift in shifts:
                stacked, n_ncm = stack_rigid(se, ncm, COMPS[c]['gap_eq'], shift)
                counts = count_interface_bonds(stacked, n_ncm)
                A = xy_area(stacked.cell.array)
                for k, v in counts.items():
                    bonds_all[k].append(v / A)
            stats = {}
            for k, vals in bonds_all.items():
                v = np.asarray(vals)
                stats[k] = {
                    'mean': float(v.mean()),
                    'std': float(v.std()),
                    'CV_pct': float(100 * v.std() / v.mean()) if v.mean() > 0 else 0.0,
                    'min': float(v.min()),
                    'max': float(v.max()),
                }
            summary[c] = stats
            log(f"  done in {time.time()-t0:.1f}s")
            for k in ('Li-O', 'Cl-O', 'Br-O'):
                s = stats[k]
                log(f"    {k:<6}: mean={s['mean']:+.4f}  std={s['std']:.4f}  CV={s['CV_pct']:.1f}%  "
                    f"range=[{s['min']:+.4f}, {s['max']:+.4f}]")
        except Exception as e:
            log(f"  {c} FAILED: {e}")

    # Re-compute R using 1000-reg means (paper comps only)
    log(f"\n--- R using 1000-reg MEAN densities ---")
    for bond in ['Li-O', 'Cl-O', 'Br-O']:
        x = [summary[c][bond]['mean'] for c in PAPER_COMPS if c in summary]
        if len(x) < 5:
            continue
        R = pearson(x, paper)
        delta = R - V15[f'R_{bond}']
        log(f"  R({bond}) = {R:+.4f}  (v15: {V15[f'R_{bond}']:+.4f}, d={delta:+.3f})")
    return summary


# =====================================================================
# Main
# =====================================================================

def main():
    t0 = time.time()
    log("=" * 70)
    log("v27 — REMAINING EXTRAS (A, D, E, F, G, H)")
    log("=" * 70)
    summary = {}
    for label, fn in [
        ('A_phase1_crossval', phase_A_phase1_crossval),
        ('D_halogen_zfit', phase_D_halogen_zfit),
        ('E_bootstrap_R', phase_E_bootstrap_R),
        ('F_cij_vs_adhesion', phase_F_cij_vs_adhesion),
        ('G_larger_ncm5L', phase_G_larger_ncm),
        ('H_1000_reg', phase_H_1000_reg),
    ]:
        t_p = time.time()
        log(f"\n##### {label} START at t+{(t_p-t0)/60:.1f} min #####")
        try:
            summary[label] = fn()
        except Exception as e:
            log(f"  FATAL {label}: {e}")
            traceback.print_exc(file=sys.stdout)
            summary[label] = {'fatal': str(e)}
        log(f"##### {label} DONE in {(time.time()-t_p)/60:.1f} min #####")

    log(f"\n=== v27 DONE: total {(time.time()-t0)/60:.1f} min ===")
    json.dump(summary, open(RESULTS_DIR / "summary.json", 'w'), indent=2, default=str)


if __name__ == "__main__":
    main()
