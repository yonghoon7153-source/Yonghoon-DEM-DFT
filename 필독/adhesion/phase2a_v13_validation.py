"""Phase 2a v13 — comprehensive validation of v12 rigid Haruyama Wad.

User concerns about v12 results (cycle 1 ranking matched paper exp):
1. xy-shift gives nearly identical Wad → suspicious, might measure
   bulk Madelung not interface chemistry
2. Fixed gap=2.5 — comp-specific equilibrium gap could differ
3. Cell-size mismatch (Li6 7x7 vs Li5.4 5x5)
4. modelC -2.18 (Phase 1) vs +0.24 (v12) — method inconsistency
5. Strain energy potential leak

This v13 runs THREE quantitative tests:

== TEST 1: Z-scan W_max ==
For each comp, scan gap = 1.5..4.0 Å (10 gaps).
Find W_max (gap-independent metric, paper-level robust).
Compare ranking with v12 fixed gap=2.5.
If ranking matches → v12 robust.
If different → switch to W_max method.

== TEST 3: Dense xy-shift sensitivity ==
At fixed gap=2.5, 100 random xy-shifts per comp.
Statistics (mean, std, min, max) per comp.
Verify xy-shift IS actually moving atoms (sanity check).
If still all same Wad → bulk Madelung dominates.
If new variation → registry chemistry sensitivity exists.

== TEST 5: Bond-counting decomposition ==
At v12 best registry per comp, count interface contacts:
  - Li(SE)-O(NCM) bonds (cation-anion attractive)
  - Cl/Br(SE)-O(NCM) (anion-anion, repulsive)
  - S(SE)-Li(NCM) (anion-cation attractive)
  - S(SE)-Ni(NCM) (anion-cation, dispersion-like)
Cutoffs from STRUCTURE_PATHS.md (3.0 Å for Li-S etc.).
Decompose Wad signal mechanistically.

NOT included (require new input or external code):
- Test 2 (same NCM cell) → would need Li5.4 with 7x7 NCM (12% strain)
- Test 4 (multiple comp4 structures) → user needs to provide alternatives

References:
- Haruyama 2014 single + vacuum + /A
- v12 (this directory): rigid single-point baseline

CODE_INVENTORY F6: ❓ UNKNOWN — validation suite, awaiting interpretation.
"""
import os, json, time, gc
from pathlib import Path
import numpy as np
from ase.io import read, write
from ase.neighborlist import neighbor_list

# -----------------------------------------------------------------------------
COMPS = {
    'comp1':  {'se': 'comp1_slab_v2.xyz',            'ncm': 'ncm_7x7x1_3Lconv.xyz'},
    'comp2':  {'se': 'comp2_slab_v2.xyz',            'ncm': 'ncm_7x7x1_3Lconv.xyz'},
    'comp3':  {'se': 'comp3_slab_v1_PRESERVED.xyz',  'ncm': 'ncm_5x5x1_3Lconv.xyz'},
    'comp4':  {'se': 'comp4_slab_v1_PRESERVED.xyz',  'ncm': 'ncm_5x5x1_3Lconv.xyz'},
    'comp5':  {'se': 'comp5_slab_v1_PRESERVED.xyz',  'ncm': 'ncm_5x5x1_3Lconv.xyz'},
    'modelC': {'se': 'modelC_slab_v2_PRESERVED.xyz', 'ncm': 'ncm_5x5x1_3Lconv.xyz'},
}

# Test 1 — Z-scan
GAPS = [1.5, 1.8, 2.0, 2.2, 2.5, 2.8, 3.0, 3.2, 3.5, 4.0]   # Å, 10 gaps

# Test 3 — dense xy-shift
GAP_DEFAULT = 2.5
N_DENSE = 100   # vs 36 in v12

# Test 5 — bond cutoffs (from STRUCTURE_PATHS.md)
BOND_CUTOFFS = {
    ('Li', 'O'): 3.0,    # Li(SE) - O(NCM)
    ('Cl', 'O'): 3.5,    # Cl-O (vdW)
    ('Br', 'O'): 3.7,
    ('S', 'Li'): 3.0,    # S(SE) - Li(NCM)
    ('S', 'Ni'): 3.5,
    ('Li', 'Ni'): 3.5,
}

VACUUM_TOP = 30.0
RANDOM_SEED = 42

RESULTS_DIR = Path("phase2a_v13_results"); RESULTS_DIR.mkdir(exist_ok=True)
LOG_FILE = RESULTS_DIR / "progress.log"

# Reuse v12 iso energies (no need to recompute)
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
    """Rigid single-interface stack (same as v12)."""
    se_a = se.copy()
    ncm_a = ncm.copy()
    new_se_cell = se_a.cell.array.copy()
    new_se_cell[0] = ncm_a.cell.array[0]
    new_se_cell[1] = ncm_a.cell.array[1]
    se_a.set_cell(new_se_cell, scale_atoms=True)
    dx, dy = shift_frac
    shift_cart = dx * ncm_a.cell.array[0] + dy * ncm_a.cell.array[1]
    se_a.translate([shift_cart[0], shift_cart[1], 0.0])
    se_a.wrap()
    ncm_a.translate([0, 0, -ncm_a.positions[:, 2].min()])
    ncm_z_max = ncm_a.positions[:, 2].max()
    se_z_min = se_a.positions[:, 2].min()
    se_a.translate([0, 0, ncm_z_max - se_z_min + gap])
    combined = ncm_a + se_a
    new_cell = ncm_a.cell.array.copy()
    z_extent = combined.positions[:, 2].max() - combined.positions[:, 2].min()
    new_cell[2] = [0.0, 0.0, z_extent + VACUUM_TOP]
    combined.set_cell(new_cell, scale_atoms=False)
    combined.set_pbc([True, True, True])
    return combined, len(ncm_a)


def xy_area(cell):
    return float(abs(np.cross(cell[0], cell[1])[2]))


def count_interface_bonds(stacked, n_ncm, gap_window=4.5):
    """Count cross-interface contacts within gap_window of NCM_top.

    Returns dict of (sym1_se, sym2_ncm) → count, where sym1 is SE atom
    and sym2 is NCM atom, both within gap_window of the interface.
    """
    syms = stacked.get_chemical_symbols()
    pos = stacked.positions
    ncm_z_max = pos[:n_ncm, 2].max()

    # Atoms near interface (within gap_window of NCM_top z)
    near_interface = [i for i in range(len(stacked))
                       if abs(pos[i, 2] - ncm_z_max) < gap_window]

    # Build neighbor list with mixed-element cutoffs
    counts = {}
    for cutoff_pair, cutoff in BOND_CUTOFFS.items():
        sym_a, sym_b = cutoff_pair
        n_ab = 0
        for i in near_interface:
            if i >= n_ncm and syms[i] == sym_a:   # SE side
                for j in near_interface:
                    if j < n_ncm and syms[j] == sym_b:   # NCM side
                        d = stacked.get_distance(i, j, mic=True)
                        if d < cutoff:
                            n_ab += 1
            elif i < n_ncm and syms[i] == sym_a:   # also try NCM side
                for j in near_interface:
                    if j >= n_ncm and syms[j] == sym_b:   # SE side
                        d = stacked.get_distance(i, j, mic=True)
                        if d < cutoff:
                            n_ab += 1
        counts[f"{sym_a}-{sym_b}"] = n_ab
    return counts


# =============================================================================
# Test 1 — Z-scan W_max per comp
# =============================================================================
def test_1_zscan(calc, iso, comp_data):
    """Z-scan binding curve per comp. Find W_max (gap-independent metric)."""
    log("=" * 70)
    log("TEST 1: Z-scan W_max (gap = 1.5..4.0 Å, 10 gaps × 6 comps)")
    log(f"Hypothesis: if W_max ranking == v12(gap=2.5) ranking → robust")
    log("=" * 70)

    results = {}
    SHIFT0 = (0.0, 0.0)   # R1_origin only for fast Z-scan

    for comp, cd in comp_data.items():
        results[comp] = {'gaps': [], 'wads': [], 'e_ints': []}
        log(f"\n--- {comp}: Z-scan ---")
        for gap in GAPS:
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
            log(f"  {comp} gap={gap:.1f}Å  E_int={E_int:.3f}  Wad={Wad:+.3f} ({time.time()-t0:.1f}s)")

        # Find W_max
        wads = results[comp]['wads']
        i_max = int(np.argmax(wads))
        results[comp]['gap_max'] = GAPS[i_max]
        results[comp]['W_max'] = wads[i_max]
        log(f"  → {comp} W_max = {wads[i_max]:+.3f} J/m² at gap={GAPS[i_max]:.1f} Å")

    # Ranking
    log(f"\n--- Test 1 Ranking ---")
    ranked_zscan = sorted(results.items(), key=lambda x: -x[1]['W_max'])
    log("v13 W_max ranking:")
    for c, r in ranked_zscan:
        log(f"  {c:<8}: W_max = {r['W_max']:+.3f} J/m² at gap={r['gap_max']:.1f}")

    # Compare vs v12 ranking (cycle 1 numbers from log)
    v12_ranking = {'comp3': 1.107, 'comp4': 0.505, 'comp5': 0.514,
                   'comp1': 0.378, 'comp2': 0.339, 'modelC': 0.235}
    paper = {'comp3': 316, 'comp4': 298, 'comp5': 249, 'comp1': 194, 'comp2': 180}

    paper_ranked = sorted(paper.items(), key=lambda x: -x[1])
    v12_ranked = sorted(v12_ranking.items(), key=lambda x: -x[1])
    log(f"\nPaper ranking:    {[c for c, _ in paper_ranked]}")
    log(f"v12 ranking:      {[c for c, _ in v12_ranked if c != 'modelC']}")
    log(f"v13 W_max ranking: {[c for c, _ in ranked_zscan if c != 'modelC']}")

    return results


# =============================================================================
# Test 3 — Dense xy-shift at fixed gap=2.5
# =============================================================================
def test_3_dense_xyshift(calc, iso, comp_data, n_dense=N_DENSE):
    """Dense xy-shift sampling at gap=2.5. Statistics per comp."""
    log("=" * 70)
    log(f"TEST 3: Dense xy-shift @ gap={GAP_DEFAULT}Å, {n_dense} random shifts")
    log("Hypothesis: if Wad std small → bulk Madelung dominates (not interface chem)")
    log("            if Wad std large → registry-dependent chemistry exists")
    log("=" * 70)

    rng = np.random.default_rng(RANDOM_SEED)
    shifts = [(rng.uniform(0, 1), rng.uniform(0, 1)) for _ in range(n_dense)]

    results = {}
    for comp, cd in comp_data.items():
        wads = []
        log(f"\n--- {comp}: dense xy-shift ---")
        t0 = time.time()
        for i, sh in enumerate(shifts):
            stacked, n_ncm = stack_rigid(cd['se'], cd['ncm'], GAP_DEFAULT, sh)
            stacked.calc = calc
            E_int = float(stacked.get_potential_energy())
            A = xy_area(stacked.cell.array)
            E_se = iso[f"{comp}_SE_strained"]['E']
            E_ncm = iso[cd['paths']['ncm']]['E']
            Wad = (E_se + E_ncm - E_int) / A * 16.0218
            wads.append(Wad)
            if (i + 1) % 25 == 0:
                log(f"  {comp} {i+1}/{n_dense} W_avg={np.mean(wads):+.3f} std={np.std(wads):.4f}")

        results[comp] = {
            'shifts': shifts,
            'wads': wads,
            'mean': float(np.mean(wads)),
            'std': float(np.std(wads)),
            'min': float(np.min(wads)),
            'max': float(np.max(wads)),
            'range': float(np.max(wads) - np.min(wads)),
            'cv_pct': float(100 * np.std(wads) / abs(np.mean(wads))) if np.mean(wads) != 0 else 0,
            'wall_min': (time.time() - t0) / 60,
        }
        log(f"  → {comp}: mean={results[comp]['mean']:+.4f}  std={results[comp]['std']:.4f}  "
            f"range={results[comp]['range']:.4f}  CV={results[comp]['cv_pct']:.1f}%")

    return results


# =============================================================================
# Test 5 — Bond-counting decomposition at v12 best registry
# =============================================================================
def test_5_bond_decomposition(calc, iso, comp_data):
    """Count interface bonds at R1_origin for each comp. Mechanistic insight."""
    log("=" * 70)
    log("TEST 5: Bond-counting decomposition at gap=2.5, R1_origin")
    log("Cutoffs (Å):", BOND_CUTOFFS)
    log("=" * 70)

    results = {}
    SHIFT0 = (0.0, 0.0)
    for comp, cd in comp_data.items():
        log(f"\n--- {comp}: bond count ---")
        stacked, n_ncm = stack_rigid(cd['se'], cd['ncm'], GAP_DEFAULT, SHIFT0)
        # No calc needed — just geometry
        counts = count_interface_bonds(stacked, n_ncm)
        results[comp] = counts
        for k, v in counts.items():
            log(f"  {comp} {k:<10s}: {v}")

    return results


# =============================================================================
# Main
# =============================================================================
def main():
    log("=" * 70)
    log("Phase 2a v13 — validation suite (Tests 1, 3, 5)")
    log("=" * 70)

    if not V12_ISO_FILE.exists():
        log(f"ERROR: v12 iso file not found: {V12_ISO_FILE}")
        log("       Run v12 first to generate iso reference energies.")
        return

    iso = json.loads(V12_ISO_FILE.read_text())
    log(f"Loaded v12 iso energies: {len(iso)} entries")

    log("Loading UMA...")
    calc = make_calc()
    log("UMA loaded.")

    comp_data = {c: {'se': read(p['se']), 'ncm': read(p['ncm']), 'paths': p}
                 for c, p in COMPS.items()}

    full_results = {}
    t_start = time.time()

    # Test 1
    full_results['test_1_zscan'] = test_1_zscan(calc, iso, comp_data)
    json.dump(full_results, open(RESULTS_DIR / "test_results.json", 'w'), indent=2, default=list)
    log(f"\nTest 1 done. Cumulative time: {(time.time()-t_start)/60:.1f} min")

    # Test 3
    full_results['test_3_dense_xyshift'] = test_3_dense_xyshift(calc, iso, comp_data)
    json.dump(full_results, open(RESULTS_DIR / "test_results.json", 'w'), indent=2, default=list)
    log(f"Test 3 done. Cumulative time: {(time.time()-t_start)/60:.1f} min")

    # Test 5
    full_results['test_5_bond_decomposition'] = test_5_bond_decomposition(calc, iso, comp_data)
    json.dump(full_results, open(RESULTS_DIR / "test_results.json", 'w'), indent=2, default=list)
    log(f"Test 5 done. Cumulative time: {(time.time()-t_start)/60:.1f} min")

    # Summary
    log("=" * 70)
    log("v13 VALIDATION SUMMARY")
    log("=" * 70)

    # Test 1 verdict
    z = full_results['test_1_zscan']
    z_ranked = sorted(z.items(), key=lambda x: -x[1]['W_max'])
    log("Test 1 (Z-scan W_max):")
    for c, r in z_ranked:
        log(f"  {c:<8}: W_max={r['W_max']:+.3f} at gap={r['gap_max']:.1f} Å")

    # Test 3 verdict
    log("\nTest 3 (Dense xy-shift):")
    for c in ['comp1', 'comp2', 'comp3', 'comp4', 'comp5', 'modelC']:
        s = full_results['test_3_dense_xyshift'].get(c, {})
        if s:
            log(f"  {c:<8}: mean={s['mean']:+.3f}±{s['std']:.4f}  CV={s['cv_pct']:.1f}%")

    # Test 5 verdict (bond counts)
    log("\nTest 5 (Interface bond counts at R1_origin):")
    for c in ['comp1', 'comp2', 'comp3', 'comp4', 'comp5', 'modelC']:
        b = full_results['test_5_bond_decomposition'].get(c, {})
        if b:
            log(f"  {c:<8}: {b}")

    log(f"\n=== v13 DONE: {(time.time()-t_start)/60:.1f} min ===")
    json.dump(full_results, open(RESULTS_DIR / "test_results.json", 'w'), indent=2, default=list)


if __name__ == "__main__":
    main()
