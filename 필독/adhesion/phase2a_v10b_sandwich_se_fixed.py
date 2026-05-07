"""Phase 2a v10b — Sandwich Wad + symmetric middle-layer FixAtoms (NCM + SE).

Diagnosis from v10 (cycle 1, 2026-05-07):
- comp1 (Li6) Wad=+2.057 J/m² (Li_mig top=23) — Camacho-Forero scale OK
- comp3 (Li5.4) Wad=-0.058 J/m² (Li_mig top=8) — vacancy effect REVERSED
- Root cause: SE no FixAtoms → Li6 high Li density migrates more → high apparent Wad
  (intermixing energy dominates, not surface chemistry). Li5.4 vacancy = fewer Li
  → less migration → low Wad. v5 paper's vacancy-anchor mechanism lost.

v10b fix: SE middle 1/3 FixAtoms (preserves bulk SE structure) + NCM middle 1/3
FixAtoms (already in v10). Both interfaces (direct + PBC) have free surfaces on
both sides (top 1/3 + bottom 1/3 of NCM and SE), enabling vacancy chemistry
without bulk Li intercalation.

Method elements:
- Sandwich geometry (Camacho-Forero 2020) — kept
- /(2A) normalization (Camacho-Forero 2020) — kept
- NCM middle 3 atomic layers FixAtoms (= middle 1/3 of 9 layers) — kept
- ⭐ SE middle 1/3 FixAtoms (NEW in v10b) — symmetric sandwich
- Iso slabs: vacuum 30 Å, BOTH NCM and SE iso also use middle 1/3 FixAtoms
  (consistency between iso and interface energy reference)
- LBFGS fmax=0.05 (was 0.03 in v10), steps=300 (was 400) — middle fix should
  converge faster
- Same 36 reg sampling × 6 comps round-robin

Expected (from v5 paper):
- comp1 (Li6) ~ 1.0-1.5 J/m²  (v5 paper 1.28)
- comp3 (Li5.4) ~ 1.5-2.5 J/m²  (v5 paper 2.10)
- Cross-family: Li5.4 > Li6 ✓ (vacancy chemical anchor)

Anchor: Camacho-Forero 2020 LPSCl/Li2S(001) Wadh = 1.44 J/m²
        Komatsu 2022 bulk LiNiO2/LPSCl ΔED = -424 meV/atom (most reactive NCM)

CODE_INVENTORY.md F3: ❓ UNKNOWN — pending pilot validation.
"""
import os, json, time, gc
from pathlib import Path
import numpy as np
from ase.io import read, write
from ase.optimize import LBFGS
from ase.constraints import FixAtoms

# -----------------------------------------------------------------------------
COMPS = {
    'comp1':  {'se': 'comp1_slab_v2.xyz',            'ncm': 'ncm_7x7x1_3Lconv.xyz'},
    'comp2':  {'se': 'comp2_slab_v2.xyz',            'ncm': 'ncm_7x7x1_3Lconv.xyz'},
    'comp3':  {'se': 'comp3_slab_v1_PRESERVED.xyz',  'ncm': 'ncm_5x5x1_3Lconv.xyz'},
    'comp4':  {'se': 'comp4_slab_v1_PRESERVED.xyz',  'ncm': 'ncm_5x5x1_3Lconv.xyz'},
    'comp5':  {'se': 'comp5_slab_v1_PRESERVED.xyz',  'ncm': 'ncm_5x5x1_3Lconv.xyz'},
    'modelC': {'se': 'modelC_slab_v2_PRESERVED.xyz', 'ncm': 'ncm_5x5x1_3Lconv.xyz'},
}

GAP = 2.5
VACUUM_TOP = 30.0
LBFGS_FMAX = 0.05    # was 0.03 in v10
LBFGS_STEPS = 300    # was 400 in v10

# Middle-layer fix fractions: fix atoms with z in [z_min + LO*range, z_min + HI*range]
LO_FRAC = 1.0 / 3.0
HI_FRAC = 2.0 / 3.0

HIGH_SYM = [
    ("R1_origin",   (0.0,    0.0)),
    ("R2_half_x",   (0.5,    0.0)),
    ("R3_half_y",   (0.0,    0.5)),
    ("R4_diagonal", (0.5,    0.5)),
    ("R5_hex1",     (1/3,    2/3)),
    ("R6_hex2",     (2/3,    1/3)),
]
N_RANDOM = 30
RANDOM_SEED = 42

RESULTS_DIR = Path("phase2a_v10b_results"); RESULTS_DIR.mkdir(exist_ok=True)
LOG_FILE    = RESULTS_DIR / "progress.log"
RESULT_FILE = RESULTS_DIR / "wad_results.json"
ISO_FILE    = RESULTS_DIR / "E_iso.json"


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


def find_middle_indices(atoms, idx_start, idx_end, lo_frac=LO_FRAC, hi_frac=HI_FRAC):
    """Indices of atoms in [idx_start, idx_end) with z in middle band of that group."""
    z = atoms.positions[idx_start:idx_end, 2]
    if len(z) == 0:
        return []
    z_min, z_max = z.min(), z.max()
    z_lo = z_min + (z_max - z_min) * lo_frac
    z_hi = z_min + (z_max - z_min) * hi_frac
    return [i for i in range(idx_start, idx_end)
            if z_lo <= atoms.positions[i, 2] <= z_hi]


def fix_iso_middle(atoms):
    """For iso slab (no other atoms): fix middle 1/3 along z."""
    idx = find_middle_indices(atoms, 0, len(atoms))
    atoms.set_constraint(FixAtoms(indices=idx))
    return len(idx)


def fix_stack_symmetric_middle(stacked, n_ncm):
    """For sandwich: fix NCM middle 1/3 AND SE middle 1/3 (symmetric)."""
    ncm_idx = find_middle_indices(stacked, 0, n_ncm)
    se_idx = find_middle_indices(stacked, n_ncm, len(stacked))
    stacked.set_constraint(FixAtoms(indices=ncm_idx + se_idx))
    return len(ncm_idx) + len(se_idx), len(ncm_idx), len(se_idx)


def stack_v10_sandwich(se, ncm, gap, shift_frac):
    """Sandwich stack: NCM | gap | SE | gap (via PBC z) → 2 interfaces."""
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
    new_cell[2] = [0.0, 0.0, z_extent + gap]
    combined.set_cell(new_cell, scale_atoms=False)
    combined.set_pbc([True, True, True])
    return combined, len(ncm_a)


def strained_se_iso(se, ncm):
    """Build SE iso slab strained to NCM lattice with vacuum (FixAtoms applied later)."""
    se_a = se.copy()
    new_cell = se_a.cell.array.copy()
    new_cell[0] = ncm.cell.array[0]
    new_cell[1] = ncm.cell.array[1]
    se_a.set_cell(new_cell, scale_atoms=True)
    return add_vacuum(se_a, VACUUM_TOP)


def xy_area(cell):
    return float(abs(np.cross(cell[0], cell[1])[2]))


def main():
    rng = np.random.default_rng(RANDOM_SEED)
    RANDOM_REG = [(f"rand_{i+1:03d}", (rng.uniform(0, 1), rng.uniform(0, 1)))
                  for i in range(N_RANDOM)]
    ALL_REG = HIGH_SYM + RANDOM_REG

    log("=" * 70)
    log("Phase 2a v10b — Sandwich Wad + symmetric middle FixAtoms (NCM + SE)")
    log("Anchors: Camacho-Forero 2020 (slab) + Komatsu 2022 (bulk)")
    log(f"Geometry: sandwich (no top vacuum at interface)")
    log(f"FixAtoms: NCM middle 1/3 + SE middle 1/3 (BOTH bulk preserved, surfaces free)")
    log(f"Wad = (E_se_iso + E_ncm_iso - E_int) / (2 A)")
    log(f"LBFGS fmax={LBFGS_FMAX}, steps={LBFGS_STEPS}, gap={GAP} A")
    log(f"Round-robin: {len(COMPS)} comps x {len(ALL_REG)} regs = "
        f"{len(COMPS)*len(ALL_REG)} interfaces")
    log(f"CUDA_VISIBLE_DEVICES={os.environ.get('CUDA_VISIBLE_DEVICES')}")
    log("=" * 70)

    log("Loading UMA...")
    calc = make_calc()
    log("UMA loaded.")

    results = json.loads(RESULT_FILE.read_text()) if RESULT_FILE.exists() else {}
    iso = json.loads(ISO_FILE.read_text()) if ISO_FILE.exists() else {}

    # ---- Stage A — Iso slabs (NCM + SE both with middle 1/3 fix) -------------
    log("=== Stage A: Iso slabs (BOTH NCM and SE: middle 1/3 FixAtoms) ===")
    ncm_done = set()
    for comp, paths in COMPS.items():
        if paths['ncm'] in ncm_done:
            continue
        if paths['ncm'] not in iso:
            ncm = read(paths['ncm'])
            ncm = add_vacuum(ncm, VACUUM_TOP)
            n_fix = fix_iso_middle(ncm)
            ncm.calc = calc
            log(f"  NCM {paths['ncm']}: n={len(ncm)}, fix middle {n_fix} ({100*n_fix/len(ncm):.1f}%)")
            t0 = time.time()
            opt = LBFGS(ncm, logfile=None)
            opt.run(fmax=LBFGS_FMAX, steps=LBFGS_STEPS)
            E = float(ncm.get_potential_energy())
            iso[paths['ncm']] = {
                'E': E, 'n': len(ncm), 'type': 'NCM_iso_middle_1_3',
                'n_fixed': n_fix, 'lbfgs_steps': opt.nsteps,
                'wall_min': (time.time() - t0) / 60,
            }
            write(str(RESULTS_DIR / f"iso_{paths['ncm'].replace('.xyz', '')}.xyz"), ncm)
            ISO_FILE.write_text(json.dumps(iso, indent=2))
            log(f"    -> E={E:.4f} ({(time.time()-t0)/60:.1f} min, steps={opt.nsteps})")
        ncm_done.add(paths['ncm'])

    for comp, paths in COMPS.items():
        key = f"{comp}_SE_strained"
        if key in iso:
            continue
        se = read(paths['se'])
        ncm = read(paths['ncm'])
        se_str = strained_se_iso(se, ncm)
        n_fix = fix_iso_middle(se_str)
        se_str.calc = calc
        log(f"  SE {comp}: n={len(se_str)}, fix middle {n_fix} ({100*n_fix/len(se_str):.1f}%)")
        t0 = time.time()
        opt = LBFGS(se_str, logfile=None)
        opt.run(fmax=LBFGS_FMAX, steps=LBFGS_STEPS)
        E = float(se_str.get_potential_energy())
        iso[key] = {
            'E': E, 'n': len(se_str), 'type': 'SE_iso_middle_1_3',
            'n_fixed': n_fix, 'lbfgs_steps': opt.nsteps,
            'wall_min': (time.time() - t0) / 60,
        }
        write(str(RESULTS_DIR / f"iso_{comp}_SE_strained.xyz"), se_str)
        ISO_FILE.write_text(json.dumps(iso, indent=2))
        log(f"    -> E={E:.4f} ({(time.time()-t0)/60:.1f} min, steps={opt.nsteps})")

    # ---- Stage B — Round-robin sandwich --------------------------------------
    log(f"=== Stage B: SANDWICH @ d={GAP} A, NCM middle 1/3 + SE middle 1/3 FixAtoms ===")
    total = len(COMPS) * len(ALL_REG)
    done = 0
    t_start = time.time()

    comp_data = {c: {'se': read(p['se']), 'ncm': read(p['ncm']), 'paths': p}
                 for c, p in COMPS.items()}
    for c in COMPS:
        (RESULTS_DIR / c).mkdir(exist_ok=True)
        results.setdefault(c, {})

    for reg_idx, (reg_name, shift) in enumerate(ALL_REG):
        log(f"\n--- Cycle {reg_idx+1}/{len(ALL_REG)}: {reg_name} ---")
        for comp, cd in comp_data.items():
            xyz_relaxed = RESULTS_DIR / comp / f"{reg_name}_iface.xyz"
            if reg_name in results[comp] and xyz_relaxed.exists():
                done += 1
                continue
            try:
                t0 = time.time()
                stacked, n_ncm = stack_v10_sandwich(cd['se'], cd['ncm'], GAP, shift)
                n_fix_total, n_fix_ncm, n_fix_se = fix_stack_symmetric_middle(stacked, n_ncm)
                stacked.calc = calc
                opt = LBFGS(stacked, logfile=None)
                opt.run(fmax=LBFGS_FMAX, steps=LBFGS_STEPS)
                E_int = float(stacked.get_potential_energy())
                steps = opt.nsteps
                write(str(xyz_relaxed), stacked)

                A = xy_area(stacked.cell.array)
                E_se = iso[f"{comp}_SE_strained"]['E']
                E_ncm = iso[cd['paths']['ncm']]['E']
                Wad = (E_se + E_ncm - E_int) / (2 * A) * 16.0218

                # Diagnostic Li migration (top-iface, pbc-iface)
                syms = stacked.get_chemical_symbols()
                ncm_z_max = float(stacked.positions[:n_ncm, 2].max())
                cell_z = float(stacked.cell.array[2, 2])
                li_mig_top = sum(1 for i in range(n_ncm, len(stacked))
                                 if syms[i] == 'Li'
                                 and stacked.positions[i, 2] < ncm_z_max - 1.0)
                li_mig_pbc = sum(1 for i in range(n_ncm, len(stacked))
                                 if syms[i] == 'Li'
                                 and stacked.positions[i, 2] > cell_z - 1.0)

                results[comp][reg_name] = {
                    'shift': list(shift),
                    'E_int': E_int,
                    'E_se_iso': E_se,
                    'E_ncm_iso': E_ncm,
                    'Wad_J_per_m2': Wad,
                    'A_A2': A,
                    'n_atoms': len(stacked),
                    'n_fixed': n_fix_total,
                    'n_fix_ncm': n_fix_ncm,
                    'n_fix_se': n_fix_se,
                    'cell_z_A': cell_z,
                    'lbfgs_steps': steps,
                    'li_mig_top_iface': li_mig_top,
                    'li_mig_pbc_iface': li_mig_pbc,
                    'wall_min': (time.time() - t0) / 60,
                }
                done += 1
                eta = (time.time() - t_start) / done * (total - done)
                wln = ""
                if li_mig_top > 0 or li_mig_pbc > 0:
                    wln = f" Li_mig top={li_mig_top} pbc={li_mig_pbc}"
                log(f"  [{done}/{total}] {comp}/{reg_name} steps={steps} "
                    f"E_int={E_int:.3f} Wad={Wad:+.3f}{wln} "
                    f"({(time.time()-t0)/60:.1f}min) ETA={eta/3600:.1f}h")

                if done % 3 == 0:
                    RESULT_FILE.write_text(json.dumps(results, indent=2))
                    gc.collect()
            except Exception as e:
                log(f"  FAIL {comp}/{reg_name}: {e}")
                import traceback
                traceback.print_exc()
                results[comp][reg_name] = {'error': str(e)}
        RESULT_FILE.write_text(json.dumps(results, indent=2))

    log(f"=== Phase 2a v10b DONE: {done}/{total} in "
        f"{(time.time()-t_start)/3600:.1f}h ===")


if __name__ == "__main__":
    main()
