"""Phase 2a v12 — Rigid Haruyama single interface (NO relaxation, single-point E only).

Lessons from v9/v10/v10b/v11 ALL FAILED cross-family:
- v9 cleavage:   comp1=1.43, comp3=0.82  → Li6 > Li5.4 ❌
- v10 sandwich:  comp1=2.06, comp3=-0.06 → Li6 >> Li5.4 ❌
- v10b sandwich+SE-fix: comp1=1.96, comp3=0.22, comp4=-0.28 → Li6 > Li5.4 ❌
- v11 Haruyama single: comp1=7.85, comp3=4.22, comp4=2.60 → Li6 > Li5.4 ❌

CONSISTENT PATTERN across 4 methods + 4 geometries:
  Li6 has more Li intermixing (18-23 atoms) → "binding" inflated
  Li5.4 has less migration (0-8 atoms) → real chemistry only
  → Li intermixing artifact dominates over vacancy chemical anchor

v12 hypothesis: REMOVE relaxation entirely → no Li migration possible →
  pure chemistry/electrostatic signal at fixed initial geometry.
  If vacancy effect is real at atomic level, it should appear here.
  If still inverted, MLIP single-grain Wad cannot capture vacancy at all.

References (필독/literature/):
- ⭐ Haruyama 2014 — single interface + vacuum + /A
- Komatsu 2022 — bulk LiNiO2/LPSCl ΔED = -424 meV/atom
- Phase 1 (existing) — rigid Z-scan binding curve method A shows Li5.4 > Li6:
   comp3=1.49, comp4=0.69, comp5=0.83  vs  comp1=0.31, comp2=0.23

v12 method elements:
1. SINGLE interface + vacuum 30 Å (Haruyama §2.1)
2. Wad = (E_iso_NCM + E_iso_SE - E_int) / A   [single-point, single interface]
3. NCM 3L conv (proper structure)
4. ⭐ NO LBFGS — single-point energy only at gap=2.5 Å
5. FixAtoms not needed (no atomic movement happens)
6. Iso slabs: also single-point (consistency with interface)
7. 36 reg sampling × 6 comps round-robin

Time estimate: ~10 sec/interface × 216 = ~36 min total (vs v11 1.5 day)

CODE_INVENTORY F5: ❓ UNKNOWN — pending pilot.
"""
import os, json, time, gc
from pathlib import Path
import numpy as np
from ase.io import read, write

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
VACUUM_TOP = 30.0     # Å (UMA OOD safety)

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

RESULTS_DIR = Path("phase2a_v12_results"); RESULTS_DIR.mkdir(exist_ok=True)
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


def stack_v12_rigid(se, ncm, gap, shift_frac):
    """Single interface (Haruyama-style) — vacuum on top of SE. No relaxation."""
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


def strained_se_iso(se, ncm):
    """SE iso strained to NCM lateral lattice + vacuum. NO relaxation."""
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
    log("Phase 2a v12 — Rigid Haruyama single interface (NO relaxation)")
    log("Test: does atomic chemistry alone (no Li migration) capture vacancy effect?")
    log(f"Geometry: SINGLE + vacuum {VACUUM_TOP} A; Wad = (E_se+E_ncm-E_int)/A; gap={GAP} A")
    log("Single-point energy only — no LBFGS, no movement, no migration possible")
    log(f"Round-robin: {len(COMPS)} x {len(ALL_REG)} = {len(COMPS)*len(ALL_REG)} interfaces")
    log(f"CUDA_VISIBLE_DEVICES={os.environ.get('CUDA_VISIBLE_DEVICES')}")
    log("=" * 70)

    log("Loading UMA...")
    calc = make_calc()
    log("UMA loaded.")

    results = json.loads(RESULT_FILE.read_text()) if RESULT_FILE.exists() else {}
    iso = json.loads(ISO_FILE.read_text()) if ISO_FILE.exists() else {}

    # -------------------------------------------------------------------------
    # Stage A — Iso slabs (NO RELAXATION, single-point E only)
    # -------------------------------------------------------------------------
    log("=== Stage A: Iso slabs (single-point, no relaxation) ===")
    ncm_done = set()
    for comp, paths in COMPS.items():
        if paths['ncm'] in ncm_done:
            continue
        if paths['ncm'] not in iso:
            ncm = read(paths['ncm'])
            ncm = add_vacuum(ncm, VACUUM_TOP)
            ncm.calc = calc
            log(f"  NCM {paths['ncm']}: n={len(ncm)} (single-point)")
            t0 = time.time()
            E = float(ncm.get_potential_energy())
            iso[paths['ncm']] = {
                'E': E, 'n': len(ncm), 'type': 'NCM_iso_rigid_no_relax',
                'wall_min': (time.time() - t0) / 60,
            }
            write(str(RESULTS_DIR / f"iso_{paths['ncm'].replace('.xyz', '')}.xyz"), ncm)
            ISO_FILE.write_text(json.dumps(iso, indent=2))
            log(f"    -> E={E:.4f} ({(time.time()-t0):.1f}s)")
        ncm_done.add(paths['ncm'])

    for comp, paths in COMPS.items():
        key = f"{comp}_SE_strained"
        if key in iso:
            continue
        se = read(paths['se'])
        ncm = read(paths['ncm'])
        se_str = strained_se_iso(se, ncm)
        se_str.calc = calc
        log(f"  SE {comp}: n={len(se_str)} (single-point, strained)")
        t0 = time.time()
        E = float(se_str.get_potential_energy())
        iso[key] = {
            'E': E, 'n': len(se_str), 'type': 'SE_iso_rigid_no_relax',
            'wall_min': (time.time() - t0) / 60,
        }
        write(str(RESULTS_DIR / f"iso_{comp}_SE_strained.xyz"), se_str)
        ISO_FILE.write_text(json.dumps(iso, indent=2))
        log(f"    -> E={E:.4f} ({(time.time()-t0):.1f}s)")

    # -------------------------------------------------------------------------
    # Stage B — Round-robin single interface, single-point E
    # -------------------------------------------------------------------------
    log(f"=== Stage B: RIGID single interface @ d={GAP} A (single-point E) ===")
    log("No LBFGS, no relaxation, no atomic movement — pure chemistry signal")
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
                stacked, n_ncm = stack_v12_rigid(cd['se'], cd['ncm'], GAP, shift)
                stacked.calc = calc
                # ⭐ NO LBFGS — single-point only
                E_int = float(stacked.get_potential_energy())
                write(str(xyz_relaxed), stacked)

                A = xy_area(stacked.cell.array)
                E_se = iso[f"{comp}_SE_strained"]['E']
                E_ncm = iso[cd['paths']['ncm']]['E']
                Wad = (E_se + E_ncm - E_int) / A * 16.0218

                results[comp][reg_name] = {
                    'shift': list(shift),
                    'E_int': E_int, 'E_se_iso': E_se, 'E_ncm_iso': E_ncm,
                    'Wad_J_per_m2': Wad,
                    'A_A2': A, 'n_atoms': len(stacked),
                    'wall_sec': (time.time() - t0),
                }
                done += 1
                eta = (time.time() - t_start) / done * (total - done)
                log(f"  [{done}/{total}] {comp}/{reg_name} "
                    f"E_int={E_int:.3f} Wad={Wad:+.3f} "
                    f"({(time.time()-t0):.1f}s) ETA={eta/60:.1f}min")

                if done % 6 == 0:
                    RESULT_FILE.write_text(json.dumps(results, indent=2))
                    gc.collect()
            except Exception as e:
                log(f"  FAIL {comp}/{reg_name}: {e}")
                import traceback
                traceback.print_exc()
                results[comp][reg_name] = {'error': str(e)}
        RESULT_FILE.write_text(json.dumps(results, indent=2))

    log(f"=== Phase 2a v12 DONE: {done}/{total} in {(time.time()-t_start)/60:.1f}min ===")


if __name__ == "__main__":
    main()
