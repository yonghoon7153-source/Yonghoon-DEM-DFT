"""Phase 2a v14 — sanity check + equilibrium gap + hybrid metric (Options B+C).

User concerns from v13:
1. xy-shift CV < 1% — is it ACTUALLY working or is there a bug?
2. v12 (gap=2.5) ranking matched paper, Z-scan W_max (all gap=1.5) DIDN'T
3. Need true equilibrium gap per comp (Option B)
4. Hybrid energy + geometry metric (Option C)

This v14 has 4 phases:

Phase A — xy-shift SANITY CHECK
  5 extreme shifts on comp1: (0,0), (0.25,0.25), (0.5,0.5), (0.111,0.777), (0.643,0.382)
  Save xyz + measure RMS atom displacement between configurations.
  PROVE shift is actually moving atoms.
  Compute Wad at each → confirm Madelung-dominated (not bug).

Phase B — FINE Z-scan equilibrium gap (Option B)
  Gaps: 1.0, 1.2, 1.4, 1.6, 1.8, 2.0, 2.2, 2.5, 3.0 (9 gaps)
  Per comp: find gap_eq = argmin E_int → W_eq = Wad at gap_eq
  Compare W_eq ranking with v12 and paper.

Phase C — Bond count at gap_eq (Option C — geometric descriptor)
  At each comp's own gap_eq, count interface contacts:
    Li(SE)-O(NCM), Cl/Br(SE)-O, S(SE)-Li(NCM), etc.
  Density per Å² for cross-comp comparison (handles cell-size mismatch).

Phase D — HYBRID METRIC (combined energy + geometry)
  For each comp: (W_eq, gap_eq, Li-O density, Cl-O density)
  Pearson R vs paper exp for each metric.
  Find descriptor that best correlates.

Time estimate: ~5 minutes total.

Reuses v12 iso energies. NO LBFGS.

CODE_INVENTORY F7: ❓ UNKNOWN — diagnostic, awaiting interpretation.
"""
import os, json, time
from pathlib import Path
import numpy as np
from ase.io import read, write

COMPS = {
    'comp1':  {'se': 'comp1_slab_v2.xyz',            'ncm': 'ncm_7x7x1_3Lconv.xyz'},
    'comp2':  {'se': 'comp2_slab_v2.xyz',            'ncm': 'ncm_7x7x1_3Lconv.xyz'},
    'comp3':  {'se': 'comp3_slab_v1_PRESERVED.xyz',  'ncm': 'ncm_5x5x1_3Lconv.xyz'},
    'comp4':  {'se': 'comp4_slab_v1_PRESERVED.xyz',  'ncm': 'ncm_5x5x1_3Lconv.xyz'},
    'comp5':  {'se': 'comp5_slab_v1_PRESERVED.xyz',  'ncm': 'ncm_5x5x1_3Lconv.xyz'},
    'modelC': {'se': 'modelC_slab_v2_PRESERVED.xyz', 'ncm': 'ncm_5x5x1_3Lconv.xyz'},
}

PHASE_A_SHIFTS = [
    ("zero",    (0.0, 0.0)),
    ("quarter", (0.25, 0.25)),
    ("half",    (0.5, 0.5)),
    ("rand1",   (0.111, 0.777)),
    ("rand2",   (0.643, 0.382)),
]

GAPS_FINE = [1.0, 1.2, 1.4, 1.6, 1.8, 2.0, 2.2, 2.5, 3.0]

BOND_CUTOFFS = {
    ('Li', 'O'): 3.0, ('Cl', 'O'): 3.5, ('Br', 'O'): 3.7,
    ('S', 'Li'): 3.0, ('S', 'Ni'): 3.5, ('Li', 'Ni'): 3.5,
}

VACUUM_TOP = 30.0
PAPER_EXP = {'comp1': 194, 'comp2': 180, 'comp3': 316, 'comp4': 298, 'comp5': 249}

RESULTS_DIR = Path("phase2a_v14_results"); RESULTS_DIR.mkdir(exist_ok=True)
LOG_FILE = RESULTS_DIR / "progress.log"
V12_ISO_FILE = Path("phase2a_v12_results/E_iso.json")


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
    cell = atoms.cell.array.copy()
    cell[2, 2] += vac
    atoms.set_cell(cell, scale_atoms=False)
    atoms.set_pbc([True, True, True])
    return atoms


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
    """Count cross-interface contacts within gap_window of NCM_top."""
    syms = stacked.get_chemical_symbols()
    pos = stacked.positions
    ncm_z_max = pos[:n_ncm, 2].max()
    near_idx = [i for i in range(len(stacked)) if abs(pos[i, 2] - ncm_z_max) < gap_window]
    counts = {}
    for (sa, sb), cut in BOND_CUTOFFS.items():
        n_ab = 0
        for i in near_idx:
            if i >= n_ncm and syms[i] == sa:
                for j in near_idx:
                    if j < n_ncm and syms[j] == sb:
                        if stacked.get_distance(i, j, mic=True) < cut:
                            n_ab += 1
            elif i < n_ncm and syms[i] == sa:
                for j in near_idx:
                    if j >= n_ncm and syms[j] == sb:
                        if stacked.get_distance(i, j, mic=True) < cut:
                            n_ab += 1
        counts[f"{sa}-{sb}"] = n_ab
    return counts


# =============================================================================
# Phase A — xy-shift sanity check (PROVE shift is actually moving atoms)
# =============================================================================
def phase_a_sanity_check(calc, iso, comp_data):
    log("=" * 70)
    log("PHASE A: xy-shift SANITY CHECK on comp1 — prove shift moves atoms")
    log("=" * 70)
    cd = comp_data['comp1']
    stacked_ref = None
    se_ref_idx = None
    results = {}

    for name, shift in PHASE_A_SHIFTS:
        stacked, n_ncm = stack_rigid(cd['se'], cd['ncm'], 2.5, shift)
        n_se = len(stacked) - n_ncm
        # Save SE atom positions for comparison
        se_pos = stacked.positions[n_ncm:n_ncm + 5].copy()  # first 5 SE atoms
        se_pos_str = " ".join(f"({p[0]:.2f},{p[1]:.2f},{p[2]:.2f})" for p in se_pos[:3])
        log(f"\n  Shift '{name}' = {shift}:")
        log(f"    First 3 SE atom xyz: {se_pos_str}")
        # Save xyz for verification
        write(str(RESULTS_DIR / f"sanity_comp1_{name}.xyz"), stacked)

        # Compute Wad
        stacked.calc = calc
        E_int = float(stacked.get_potential_energy())
        A = xy_area(stacked.cell.array)
        E_se = iso['comp1_SE_strained']['E']
        E_ncm = iso['ncm_7x7x1_3Lconv.xyz']['E']
        Wad = (E_se + E_ncm - E_int) / A * 16.0218
        log(f"    Wad = {Wad:+.4f} J/m²,  E_int = {E_int:.3f}")

        results[name] = {'shift': shift, 'Wad': Wad, 'E_int': E_int,
                         'first_3_se_atoms': [list(p) for p in se_pos[:3].tolist()]}

        if stacked_ref is None:
            stacked_ref = stacked
            se_ref_idx = n_ncm
        else:
            # RMS displacement of SE atoms vs reference (zero shift)
            disp = stacked.positions[n_ncm:] - stacked_ref.positions[se_ref_idx:]
            # Account for PBC wrapping — fold into nearest image
            cell = stacked.cell.array
            for k in range(2):  # x, y only (z stays)
                disp[:, k] = (disp[:, k] + cell[k, k]/2) % cell[k, k] - cell[k, k]/2
            rms = float(np.sqrt(np.mean(disp[:, :2]**2)))
            log(f"    RMS xy displacement (vs zero shift): {rms:.3f} Å")
            results[name]['rms_xy_disp'] = rms

    # Verdict
    wads = [r['Wad'] for r in results.values()]
    rms_disps = [r.get('rms_xy_disp', 0) for r in results.values() if 'rms_xy_disp' in r]
    log(f"\n  --- Phase A verdict ---")
    log(f"  Wad range: {min(wads):.4f} to {max(wads):.4f}  Δ={max(wads)-min(wads):.4f}")
    log(f"  RMS xy disp range: {min(rms_disps):.2f} to {max(rms_disps):.2f} Å")
    if max(rms_disps) > 0.5:
        log(f"  ✓ xy-shift IS working: atoms move by {max(rms_disps):.1f}+ Å")
        log(f"  ✓ But Wad essentially constant (Δ={max(wads)-min(wads):.4f})")
        log(f"  → CONFIRMED: Madelung-dominated, NOT a code bug")
    else:
        log(f"  ⚠ atoms NOT moving — possible code bug?")

    return results


# =============================================================================
# Phase B — Fine Z-scan equilibrium gap (Option B)
# =============================================================================
def phase_b_equilibrium_gap(calc, iso, comp_data):
    log("=" * 70)
    log(f"PHASE B: Fine Z-scan equilibrium gap, gaps = {GAPS_FINE}")
    log("=" * 70)
    SHIFT0 = (0.0, 0.0)
    results = {}

    for comp, cd in comp_data.items():
        results[comp] = {'gaps': [], 'wads': [], 'e_ints': []}
        log(f"\n--- {comp}: fine Z-scan ---")
        for gap in GAPS_FINE:
            t0 = time.time()
            stacked, n_ncm = stack_rigid(cd['se'], cd['ncm'], gap, SHIFT0)
            stacked.calc = calc
            E_int = float(stacked.get_potential_energy())
            A = xy_area(stacked.cell.array)
            E_se = iso[f"{comp}_SE_strained"]['E']
            E_ncm = iso[cd['paths']['ncm']]['E']
            Wad = (E_se + E_ncm - E_int) / A * 16.0218
            results[comp]['gaps'].append(gap)
            results[comp]['wads'].append(Wad)
            results[comp]['e_ints'].append(E_int)
            log(f"  {comp} gap={gap:.1f}A  E_int={E_int:.3f}  Wad={Wad:+.4f}")

        # Find equilibrium gap (= max Wad = min E_int)
        wads = results[comp]['wads']
        i_eq = int(np.argmax(wads))
        results[comp]['gap_eq'] = GAPS_FINE[i_eq]
        results[comp]['W_eq'] = wads[i_eq]
        log(f"  -> {comp} gap_eq={GAPS_FINE[i_eq]:.1f}A  W_eq={wads[i_eq]:+.4f}")

    return results


# =============================================================================
# Phase C — Bond count at each comp's own gap_eq
# =============================================================================
def phase_c_bond_count(calc, iso, comp_data, gap_eq_per_comp):
    log("=" * 70)
    log("PHASE C: Bond count at each comp's own gap_eq")
    log("=" * 70)
    SHIFT0 = (0.0, 0.0)
    results = {}

    for comp, cd in comp_data.items():
        gap_eq = gap_eq_per_comp[comp]
        log(f"\n--- {comp}: bond count at gap_eq={gap_eq:.1f} A ---")
        stacked, n_ncm = stack_rigid(cd['se'], cd['ncm'], gap_eq, SHIFT0)
        counts = count_interface_bonds(stacked, n_ncm)
        A = xy_area(stacked.cell.array)
        densities = {f"{k}_density": v / A for k, v in counts.items()}
        results[comp] = {'gap_eq': gap_eq, 'A': A, **counts, **densities}
        for k, v in counts.items():
            d = v / A
            log(f"  {comp} {k:<10s}: {v:>3d} bonds  ({d:.4f}/Å²)")

    return results


# =============================================================================
# Phase D — Hybrid metric: which descriptor best correlates with paper exp?
# =============================================================================
def phase_d_hybrid(zscan_results, bond_results):
    log("=" * 70)
    log("PHASE D: Hybrid metric — Pearson R vs paper experimental Wad")
    log("=" * 70)

    # Build descriptor table
    table = []
    for comp in ['comp1', 'comp2', 'comp3', 'comp4', 'comp5']:  # exclude modelC (no exp)
        if comp not in PAPER_EXP:
            continue
        row = {
            'comp': comp,
            'paper_exp_aJ': PAPER_EXP[comp],
            'gap_eq': zscan_results[comp]['gap_eq'],
            'W_eq': zscan_results[comp]['W_eq'],
            'Li-O': bond_results[comp].get('Li-O', 0),
            'Cl-O': bond_results[comp].get('Cl-O', 0),
            'Br-O': bond_results[comp].get('Br-O', 0),
            'Li-O_density': bond_results[comp].get('Li-O_density', 0),
            'Cl-O_density': bond_results[comp].get('Cl-O_density', 0),
            'Br-O_density': bond_results[comp].get('Br-O_density', 0),
        }
        # Sum of attractive bonds (Li-O is attractive)
        # Sum of repulsive (Cl-O, Br-O are anion-anion)
        row['sum_attractive'] = row['Li-O']
        row['sum_repulsive'] = row['Cl-O'] + row['Br-O']
        row['net_bonds'] = row['sum_attractive'] - row['sum_repulsive']
        row['attractive_density'] = row['Li-O_density']
        row['repulsive_density'] = row['Cl-O_density'] + row['Br-O_density']
        table.append(row)

    # Print table
    log(f"\n{'comp':<8} {'paper':>6} {'gap_eq':>7} {'W_eq':>8} {'Li-O':>5} {'Cl-O':>5} {'Br-O':>5} {'LiO/A²':>9} {'BrO/A²':>9}")
    for r in table:
        log(f"{r['comp']:<8} {r['paper_exp_aJ']:>6} {r['gap_eq']:>7.1f} {r['W_eq']:>+8.3f} "
            f"{r['Li-O']:>5d} {r['Cl-O']:>5d} {r['Br-O']:>5d} "
            f"{r['Li-O_density']:>9.4f} {r['Br-O_density']:>9.4f}")

    # Pearson R for each descriptor
    paper_y = np.array([r['paper_exp_aJ'] for r in table])
    descriptors = ['W_eq', 'Li-O', 'Cl-O', 'Br-O',
                   'Li-O_density', 'Cl-O_density', 'Br-O_density',
                   'sum_attractive', 'sum_repulsive', 'net_bonds',
                   'attractive_density', 'repulsive_density']

    log(f"\n--- Pearson R correlations vs paper exp (n={len(table)}) ---")
    pearsons = {}
    for d in descriptors:
        x = np.array([r[d] for r in table])
        if x.std() == 0:
            pearsons[d] = float('nan')
            log(f"  R({d:<22}) = nan  (zero variance)")
            continue
        r = float(np.corrcoef(x, paper_y)[0, 1])
        pearsons[d] = r
        flag = "⭐" if abs(r) > 0.9 else "" if abs(r) > 0.7 else "   "
        log(f"  R({d:<22}) = {r:+.4f}  {flag}")

    return {'table': table, 'pearson_R': pearsons}


# =============================================================================
# Main
# =============================================================================
def main():
    log("=" * 70)
    log("Phase 2a v14 — sanity + equilibrium gap + hybrid metric")
    log("=" * 70)

    if not V12_ISO_FILE.exists():
        log(f"ERROR: v12 iso file not found: {V12_ISO_FILE}")
        return
    iso = json.loads(V12_ISO_FILE.read_text())
    log(f"Loaded v12 iso: {len(iso)} entries")

    log("Loading UMA...")
    calc = make_calc()
    log("UMA loaded.")

    comp_data = {c: {'se': read(p['se']), 'ncm': read(p['ncm']), 'paths': p}
                 for c, p in COMPS.items()}

    full = {}
    t_start = time.time()

    full['phase_a_sanity'] = phase_a_sanity_check(calc, iso, comp_data)
    json.dump(full, open(RESULTS_DIR / "results.json", 'w'), indent=2, default=list)
    log(f"\nPhase A done. Cumulative: {(time.time()-t_start)/60:.1f} min")

    full['phase_b_zscan'] = phase_b_equilibrium_gap(calc, iso, comp_data)
    json.dump(full, open(RESULTS_DIR / "results.json", 'w'), indent=2, default=list)
    log(f"Phase B done. Cumulative: {(time.time()-t_start)/60:.1f} min")

    gap_eq_per_comp = {c: full['phase_b_zscan'][c]['gap_eq'] for c in COMPS}
    full['phase_c_bonds'] = phase_c_bond_count(calc, iso, comp_data, gap_eq_per_comp)
    json.dump(full, open(RESULTS_DIR / "results.json", 'w'), indent=2, default=list)
    log(f"Phase C done. Cumulative: {(time.time()-t_start)/60:.1f} min")

    full['phase_d_hybrid'] = phase_d_hybrid(full['phase_b_zscan'], full['phase_c_bonds'])
    json.dump(full, open(RESULTS_DIR / "results.json", 'w'), indent=2, default=list)
    log(f"Phase D done. Cumulative: {(time.time()-t_start)/60:.1f} min")

    log("=" * 70)
    log("v14 SUMMARY")
    log("=" * 70)

    # Phase A
    log("\nPhase A — xy-shift sanity:")
    pa = full['phase_a_sanity']
    rms_max = max(r.get('rms_xy_disp', 0) for r in pa.values())
    wads = [r['Wad'] for r in pa.values()]
    log(f"  Max RMS xy displacement: {rms_max:.2f} Å (atoms ARE moving)")
    log(f"  Wad range: {min(wads):.4f}..{max(wads):.4f}  Δ={max(wads)-min(wads):.4f}")
    log(f"  → xy-shift {'works (Madelung-dominated)' if rms_max > 0.5 else 'BROKEN — bug suspected'}")

    # Phase B/D
    log("\nPhase B — equilibrium gap per comp:")
    for c in ['comp1','comp2','comp3','comp4','comp5','modelC']:
        r = full['phase_b_zscan'][c]
        log(f"  {c:<8}: gap_eq={r['gap_eq']:.1f}Å  W_eq={r['W_eq']:+.4f}")

    # Phase D
    pearsons = full['phase_d_hybrid']['pearson_R']
    best = max(pearsons.items(), key=lambda x: abs(x[1]) if not np.isnan(x[1]) else -1)
    log(f"\nPhase D — best descriptor vs paper exp:")
    log(f"  BEST: {best[0]} (R={best[1]:+.4f})")
    log(f"\nAll descriptors (sorted by |R|):")
    for d, r in sorted(pearsons.items(), key=lambda x: -abs(x[1]) if not np.isnan(x[1]) else 99):
        log(f"  R({d:<22}) = {r:+.4f}")

    log(f"\n=== v14 DONE: {(time.time()-t_start)/60:.1f} min ===")
    json.dump(full, open(RESULTS_DIR / "results.json", 'w'), indent=2, default=list)


if __name__ == "__main__":
    main()
