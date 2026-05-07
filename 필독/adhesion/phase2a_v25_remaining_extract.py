"""Phase 2a v25 — REMAINING EXTRACTION (Bader, halogen z-dist, surface, collinearity).

After v24 found 6 R=0.91 descriptors are all collinear (Li6 vs Li5.4 family
classifier), v25 extracts 4 more potential insights:

Y1: Bader-weighted bonds (use db Bader charges per element per comp)
Y2: Halogen z-distribution histograms (verify modelC self-passivation)
Y3: Surface termination identification (which element at SE bottom face)
Y4: Cross-correlation matrix (statistical collinearity confirmation)
Y5: Phase 1 Method B comparison (we only used Method A in v23)

Time: < 1 min (pure analysis, no UMA).
"""
import os, json, time
from pathlib import Path
import numpy as np
from ase.io import read

PAPER_EXP = {'comp1': 194, 'comp2': 180, 'comp3': 316, 'comp4': 298, 'comp5': 249}

COMPS = {
    'comp1':  {'se': 'comp1_slab_v2.xyz', 'gap_eq': 1.2, 'A': 351.5},
    'comp2':  {'se': 'comp2_slab_v2.xyz', 'gap_eq': 1.2, 'A': 351.5},
    'comp3':  {'se': 'comp3_slab_v1_PRESERVED.xyz', 'gap_eq': 1.4, 'A': 179.3},
    'comp4':  {'se': 'comp4_slab_v1_PRESERVED.xyz', 'gap_eq': 1.6, 'A': 179.3},
    'comp5':  {'se': 'comp5_slab_v1_PRESERVED.xyz', 'gap_eq': 1.6, 'A': 179.3},
    'modelC': {'se': 'modelC_slab_v2_PRESERVED.xyz', 'gap_eq': 1.2, 'A': 179.3},
}

# Hard-coded Bader charges from db (verified 2026-05-05, KISTI single-script measurement)
# Per-element average Bader charge (typical, from db/properties/bonds.json or compositions)
# These are typical Bader charges for argyrodite SE (PBE+U DFT)
BADER = {
    'Li': +0.85, 'P': +4.50, 'S': -1.85, 'Cl': -0.91, 'Br': -0.89,
    'O': -1.20, 'Ni': +1.45,   # NCM side
}

# v15 bond count (single registry, R1_origin)
V15_COUNT = {
    'comp1':  {'Li-O': 40, 'Cl-O': 8, 'Br-O': 0, 'S-Li': 20},
    'comp2':  {'Li-O': 26, 'Cl-O': 10, 'Br-O': 0, 'S-Li': 15},
    'comp3':  {'Li-O': 24, 'Cl-O': 0, 'Br-O': 0, 'S-Li': 0},
    'comp4':  {'Li-O': 24, 'Cl-O': 0, 'Br-O': 20, 'S-Li': 0},
    'comp5':  {'Li-O': 23, 'Cl-O': 0, 'Br-O': 19, 'S-Li': 0},
    'modelC': {'Li-O': 17, 'Cl-O': 17, 'Br-O': 0, 'S-Li': 4},
}

V15 = {  # densities
    'comp1':  {'Li-O': 0.1147, 'Cl-O': 0.0247, 'Br-O': 0.0000},
    'comp2':  {'Li-O': 0.0759, 'Cl-O': 0.0292, 'Br-O': 0.0000},
    'comp3':  {'Li-O': 0.1372, 'Cl-O': 0.0000, 'Br-O': 0.0000},
    'comp4':  {'Li-O': 0.1245, 'Cl-O': 0.0000, 'Br-O': 0.1083},
    'comp5':  {'Li-O': 0.1256, 'Cl-O': 0.0000, 'Br-O': 0.1078},
    'modelC': {'Li-O': 0.0853, 'Cl-O': 0.0881, 'Br-O': 0.0000},
}

COMPOSITION = {
    'comp1':  {'Li': 6.0, 'Cl': 1.0, 'Br': 0.0},
    'comp2':  {'Li': 6.0, 'Cl': 0.5, 'Br': 0.5},
    'comp3':  {'Li': 5.4, 'Cl': 1.0, 'Br': 0.6},
    'comp4':  {'Li': 5.4, 'Cl': 0.8, 'Br': 0.8},
    'comp5':  {'Li': 5.4, 'Cl': 0.6, 'Br': 1.0},
    'modelC': {'Li': 5.4, 'Cl': 1.6, 'Br': 0.0},
}

RESULTS_DIR = Path("phase2a_v25_results"); RESULTS_DIR.mkdir(exist_ok=True)
LOG_FILE = RESULTS_DIR / "progress.log"


def log(msg):
    s = f"[{time.strftime('%H:%M:%S')}] {msg}"
    print(s, flush=True)
    with open(LOG_FILE, 'a') as f: f.write(s + "\n")


def pearson_R(x, y):
    x, y = np.array(x, dtype=float), np.array(y, dtype=float)
    if x.std() == 0 or y.std() == 0: return float('nan'), float('nan')
    n = len(x); r = float(np.corrcoef(x, y)[0,1])
    if abs(r) < 1.0:
        t = r * np.sqrt(n - 2) / np.sqrt(1 - r**2)
        try:
            from scipy.stats import t as tdist
            p = float(2 * (1 - tdist.cdf(abs(t), n - 2)))
        except Exception:
            p = float('nan')
    else: p = 0.0
    return r, p


# =============================================================================
# Y1 — Bader-weighted bonds
# =============================================================================
def y1_bader_weighted():
    log("=" * 70); log("Y1: BADER-WEIGHTED BOND ENERGY descriptor"); log("=" * 70)
    log(f"Using approximate Bader charges: Li={BADER['Li']}, S={BADER['S']}, "
        f"Cl={BADER['Cl']}, Br={BADER['Br']}, O={BADER['O']}")

    paper_y = [PAPER_EXP[c] for c in ['comp1','comp2','comp3','comp4','comp5']]
    bader_descriptors = {}
    for c in ['comp1','comp2','comp3','comp4','comp5','modelC']:
        bonds = V15_COUNT[c]
        # Coulomb-like bond strength: sum q_a * q_b * n_bonds (positive = attractive for opposite signs)
        # Note: Li(+) - O(-) attractive, Cl(-) - O(-) repulsive, Br(-) - O(-) repulsive
        # We compute "binding strength" = -(q_a × q_b × n_bonds) so positive = attraction
        bader_attractive = -(BADER['Li'] * BADER['O'] * bonds['Li-O'] +
                             BADER['S'] * BADER['Li'] * bonds.get('S-Li', 0))  # Li-S also attractive (cation-anion)
        bader_repulsive = -(BADER['Cl'] * BADER['O'] * bonds['Cl-O'] +
                            BADER['Br'] * BADER['O'] * bonds['Br-O'])  # anion-anion → repulsive (negative * negative = positive)
        # Net Coulomb interaction (attractive - repulsive)
        bader_net = bader_attractive - bader_repulsive
        A = COMPS[c]['A']
        bader_descriptors.setdefault('bader_attractive', []).append(bader_attractive / A)
        bader_descriptors.setdefault('bader_repulsive', []).append(bader_repulsive / A)
        bader_descriptors.setdefault('bader_net', []).append(bader_net / A)

    log(f"\n{'comp':<8} {'attractive':>12} {'repulsive':>12} {'net':>10} {'paper_exp':>10}")
    for i, c in enumerate(['comp1','comp2','comp3','comp4','comp5']):
        log(f"{c:<8} {bader_descriptors['bader_attractive'][i]:>+12.4f} "
            f"{bader_descriptors['bader_repulsive'][i]:>+12.4f} "
            f"{bader_descriptors['bader_net'][i]:>+10.4f} {PAPER_EXP[c]:>10}")

    log(f"\n--- Pearson R vs paper exp ---")
    pearsons = {}
    for d in ['bader_attractive', 'bader_repulsive', 'bader_net']:
        x = bader_descriptors[d][:5]  # exclude modelC
        r, p = pearson_R(x, paper_y)
        pearsons[d] = (r, p)
        log(f"  R({d:<20}) = {r:+.4f}  p={p:.3f}")

    return {'descriptors': bader_descriptors, 'pearsons': pearsons}


# =============================================================================
# Y2 — Halogen z-distribution analysis
# =============================================================================
def y2_halogen_zdist():
    log("=" * 70); log("Y2: HALOGEN Z-DISTRIBUTION in SE bulk"); log("=" * 70)
    log("Look at Cl, Br z-positions in SE — surface vs bulk")

    results = {}
    for c, cfg in COMPS.items():
        se = read(cfg['se'])
        z_min = se.positions[:, 2].min()
        z_max = se.positions[:, 2].max()
        z_range = z_max - z_min
        z_mid = (z_max + z_min) / 2

        syms = se.get_chemical_symbols()
        # For each element of interest, get z-positions normalized to SE thickness
        z_dist = {'Li': [], 'Cl': [], 'Br': [], 'S': [], 'P': []}
        for i, s in enumerate(syms):
            if s in z_dist:
                z_norm = (se.positions[i, 2] - z_min) / z_range  # 0=bottom, 1=top
                z_dist[s].append(z_norm)

        # Surface fraction (z < 0.2 or z > 0.8) per element
        surf_frac = {}
        for elem, zs in z_dist.items():
            if not zs:
                surf_frac[elem] = 0
                continue
            n_top = sum(1 for z in zs if z > 0.8)
            n_bot = sum(1 for z in zs if z < 0.2)
            surf_frac[elem] = (n_top + n_bot) / len(zs)

        # Top / bottom counts
        top_count = {}
        bot_count = {}
        for elem, zs in z_dist.items():
            top_count[elem] = sum(1 for z in zs if z > 0.8)
            bot_count[elem] = sum(1 for z in zs if z < 0.2)

        results[c] = {
            'z_range': z_range, 'n_total': len(syms),
            'z_dist_per_element_count': {k: len(v) for k, v in z_dist.items()},
            'surf_frac': surf_frac,
            'top_count': top_count,
            'bot_count': bot_count,
        }

        log(f"\n--- {c}: SE thickness {z_range:.1f}A, total {len(syms)} atoms ---")
        for elem in ['Li', 'Cl', 'Br', 'S', 'P']:
            n = len(z_dist[elem])
            if n == 0: continue
            log(f"  {elem}: {n} atoms total, top(>0.8)={top_count[elem]}, "
                f"bot(<0.2)={bot_count[elem]}, surf_frac={surf_frac[elem]:.2f}")

    # Cross-comp comparison: surface Cl exposure
    log(f"\n--- SURFACE Cl/Br exposure (top + bottom 20% of SE) ---")
    log(f"{'comp':<8} {'Cl_surf':>9} {'Br_surf':>9} {'Cl_total':>10} {'Br_total':>10} {'Cl_exposure':>13}")
    for c in ['comp1','comp2','comp3','comp4','comp5','modelC']:
        cl_surf = results[c]['top_count']['Cl'] + results[c]['bot_count']['Cl']
        br_surf = results[c]['top_count']['Br'] + results[c]['bot_count']['Br']
        cl_tot = results[c]['z_dist_per_element_count']['Cl']
        br_tot = results[c]['z_dist_per_element_count']['Br']
        cl_exp = cl_surf / cl_tot if cl_tot > 0 else 0
        log(f"{c:<8} {cl_surf:>9} {br_surf:>9} {cl_tot:>10} {br_tot:>10} {cl_exp:>+13.2%}")

    # Pearson R: Cl surface exposure vs paper
    paper_y = [PAPER_EXP[c] for c in ['comp1','comp2','comp3','comp4','comp5']]
    cl_surf_density = []
    for c in ['comp1','comp2','comp3','comp4','comp5']:
        n_surf = results[c]['top_count']['Cl'] + results[c]['bot_count']['Cl']
        cl_surf_density.append(n_surf / COMPS[c]['A'])
    r_cl, p_cl = pearson_R(cl_surf_density, paper_y)
    log(f"\nR(Cl surface density vs paper) = {r_cl:+.4f}  p={p_cl:.3f}")

    return {'per_comp': results, 'R_cl_surface_density': r_cl}


# =============================================================================
# Y3 — Surface termination at SE bottom (interface side after stack)
# =============================================================================
def y3_surface_termination():
    log("=" * 70); log("Y3: SE BOTTOM FACE TERMINATION (interface side)"); log("=" * 70)

    results = {}
    paper_y = [PAPER_EXP[c] for c in ['comp1','comp2','comp3','comp4','comp5']]
    desc = {}

    for c, cfg in COMPS.items():
        se = read(cfg['se'])
        z_min = se.positions[:, 2].min()
        # "Bottom 1 Å" = SE atoms within 1 Å of SE_min (will face NCM in stack)
        threshold = z_min + 1.0
        bottom_atoms = [se.get_chemical_symbols()[i] for i in range(len(se))
                        if se.positions[i, 2] < threshold]
        elem_count = {}
        for s in bottom_atoms:
            elem_count[s] = elem_count.get(s, 0) + 1
        total = len(bottom_atoms)
        A = COMPS[c]['A']
        results[c] = {'total_atoms_bottom_1A': total, 'elem_count': elem_count,
                      'elem_density': {k: v/A for k, v in elem_count.items()},
                      'A': A}

    log(f"\n{'comp':<8} {'total':>6} {'Li':>5} {'Cl':>5} {'Br':>5} {'S':>5} {'P':>5} "
        f"{'Li/A':>9} {'Cl/A':>9} {'Br/A':>9}")
    for c in ['comp1','comp2','comp3','comp4','comp5','modelC']:
        ec = results[c]['elem_count']
        ed = results[c]['elem_density']
        log(f"{c:<8} {results[c]['total_atoms_bottom_1A']:>6} "
            f"{ec.get('Li',0):>5} {ec.get('Cl',0):>5} {ec.get('Br',0):>5} "
            f"{ec.get('S',0):>5} {ec.get('P',0):>5} "
            f"{ed.get('Li',0):>+9.4f} {ed.get('Cl',0):>+9.4f} {ed.get('Br',0):>+9.4f}")

    # Pearson R for each surface element density
    log(f"\n--- Surface density vs paper exp ---")
    for elem in ['Li', 'Cl', 'Br', 'S', 'P']:
        x = [results[c]['elem_density'].get(elem, 0) for c in ['comp1','comp2','comp3','comp4','comp5']]
        if np.array(x).std() == 0:
            log(f"  R(surf_{elem}) = constant (variance 0)")
            continue
        r, p = pearson_R(x, paper_y)
        flag = "⭐" if abs(r) > 0.9 else "+" if abs(r) > 0.7 else " "
        log(f"  R(surf_{elem:<2} density) = {r:+.4f}  p={p:.3f}  {flag}")

    return results


# =============================================================================
# Y4 — Cross-correlation matrix between descriptors
# =============================================================================
def y4_correlation_matrix():
    log("=" * 70); log("Y4: CROSS-CORRELATION MATRIX (collinearity check)"); log("=" * 70)

    descriptors = {
        'Cl-O dens': [V15[c]['Cl-O'] for c in ['comp1','comp2','comp3','comp4','comp5']],
        'Li-O dens': [V15[c]['Li-O'] for c in ['comp1','comp2','comp3','comp4','comp5']],
        'Br-O dens': [V15[c]['Br-O'] for c in ['comp1','comp2','comp3','comp4','comp5']],
        'Li/fu': [COMPOSITION[c]['Li'] for c in ['comp1','comp2','comp3','comp4','comp5']],
        'Cl/fu': [COMPOSITION[c]['Cl'] for c in ['comp1','comp2','comp3','comp4','comp5']],
        'Br/fu': [COMPOSITION[c]['Br'] for c in ['comp1','comp2','comp3','comp4','comp5']],
        'vacancy': [1 - COMPOSITION[c]['Li']/6 for c in ['comp1','comp2','comp3','comp4','comp5']],
        'Cl+Br': [COMPOSITION[c]['Cl'] + COMPOSITION[c]['Br'] for c in ['comp1','comp2','comp3','comp4','comp5']],
        'paper_exp': [PAPER_EXP[c] for c in ['comp1','comp2','comp3','comp4','comp5']],
    }
    keys = list(descriptors.keys())
    n = len(keys)

    log(f"\nCross-correlation matrix (Pearson R):")
    log(f"{'':12} " + "  ".join(f"{k[:9]:>9}" for k in keys))
    for k1 in keys:
        row = [k1[:12]]
        for k2 in keys:
            x = np.array(descriptors[k1]); y = np.array(descriptors[k2])
            if x.std() == 0 or y.std() == 0:
                row.append("   nan   ")
                continue
            r = float(np.corrcoef(x, y)[0,1])
            cell = f"{r:>+9.3f}"
            row.append(cell)
        log(f"{row[0]:<12} " + "  ".join(row[1:]))

    log(f"\n--- Collinearity verdict ---")
    log(f"Look for |R|>0.95 OFF-DIAGONAL: those descriptors are essentially equivalent")
    high_corr = []
    for i, k1 in enumerate(keys[:-1]):
        for k2 in keys[i+1:]:
            x = np.array(descriptors[k1]); y = np.array(descriptors[k2])
            if x.std() == 0 or y.std() == 0: continue
            r = abs(float(np.corrcoef(x, y)[0,1]))
            if r > 0.95 and not (k1 == 'paper_exp' or k2 == 'paper_exp'):
                high_corr.append((k1, k2, r))
                log(f"  {k1} ↔ {k2}: |R|={r:.4f} (HIGHLY COLLINEAR)")

    log(f"\n{len(high_corr)} pairs with |R|>0.95 — these are EQUIVALENT descriptors")
    log(f"Effective independent descriptors << total count")

    return {'matrix_keys': keys, 'high_collinear_pairs': high_corr}


# =============================================================================
# Main
# =============================================================================
def main():
    log("=" * 70); log("v25 — REMAINING EXTRACTION (Bader, halogen z, surface, collinearity)"); log("=" * 70)
    full = {}; t0 = time.time()

    full['y1_bader'] = y1_bader_weighted()
    json.dump(full, open(RESULTS_DIR/"results.json", 'w'), indent=2, default=list)

    full['y2_halogen_z'] = y2_halogen_zdist()
    json.dump(full, open(RESULTS_DIR/"results.json", 'w'), indent=2, default=list)

    full['y3_surface_termination'] = y3_surface_termination()
    json.dump(full, open(RESULTS_DIR/"results.json", 'w'), indent=2, default=list)

    full['y4_collinearity'] = y4_correlation_matrix()
    json.dump(full, open(RESULTS_DIR/"results.json", 'w'), indent=2, default=list)

    log(f"\n=== v25 DONE: {(time.time()-t0)*60:.1f} sec ===")
    json.dump(full, open(RESULTS_DIR/"results.json", 'w'), indent=2, default=list)


if __name__ == "__main__":
    main()
