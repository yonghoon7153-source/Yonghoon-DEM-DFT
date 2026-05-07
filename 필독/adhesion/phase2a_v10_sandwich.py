"""Phase 2a v10 — Sandwich Wad (Camacho-Forero 2020 + Komatsu 2022 anchored).

References (see 필독/literature/):
- Camacho-Forero & Balbuena, Chem. Mater. 2020, 32, 360-373 (DOI 10.1021/acs.chemmater.9b03880)
    Method anchor: SANDWICH geometry (PBC z creates 2 interfaces), no vacuum,
    full geometry relaxation, /(2A) normalization. LPSCl/Li2S(001) Wadh = 1.44 J/m².
- Komatsu et al. (NOT Sicolo), J. Phys. Chem. C 2022, 126, 17482 (DOI 10.1021/acs.jpcc.2c05336)
    Bulk thermodynamic anchor: LiNiO2/LPSCl ΔED,min,mutual = -424 meV/atom (most reactive
    NCM). Reaction products: Ni3S2 + Li2S + Li2SO4 + Li3PO4 + LiCl. Volume change:
    -11% chemical, -34% at 4.5V.

Method changes from v5 (phase2a_lbfgs_wad.py):
  (1) NCM = 3L conv (9 atomic layers, ~42.6 Å) — was 1L conv (3 atomic layers, broken)
  (2) Sandwich geometry — cell_z = z_extent + GAP (no 30 Å top vacuum at interface)
  (3) FixAtoms = NCM MIDDLE 3 atomic layers ONLY (preserves bulk reference,
      allows BOTH interfaces' chemistry — direct AND PBC). SE: no FixAtoms (Camacho-Forero).
  (4) Wad = (E_se_iso + E_ncm_iso − E_int) / (2 A) — was /A (was wrong for sandwich)
  (5) LBFGS fmax=0.03, steps=400 — was 0.05/200 (v9 saturated at 200, undercoverged)
  (6) Iso slabs keep vacuum 30 Å (UMA OOD requirement) but NCM iso also uses
      middle-layer FixAtoms for consistency with sandwich constraint.

Expected: comp1 (LiNiO2/LPSCl) v5 paper = 1.28 J/m² → v10 sandwich likely 1.5-3.0 J/m²
(Camacho-Forero LPSCl/Li2S(001) = 1.44 J/m² as scale anchor; LiNiO2 more reactive than Li2S
per Komatsu bulk thermo, expect higher Wad).

Verified inputs (CODE_INVENTORY.md F2):
  SE slabs: comp{1,2}_slab_v2.xyz (cubic), comp{3,4,5}_slab_v1_PRESERVED.xyz,
            modelC_slab_v2_PRESERVED.xyz (rhombo→pymatgen conv)
  NCM 3Lconv: ncm_7x7x1_3Lconv.xyz (Li6, 1764 at), ncm_5x5x1_3Lconv.xyz (Li5.4, 900 at)

CODE_INVENTORY.md status: ❓ UNKNOWN (untested, awaiting pilot validation).
"""
import os, json, time, gc
from pathlib import Path
import numpy as np
from ase.io import read, write
from ase.optimize import LBFGS
from ase.constraints import FixAtoms

# -----------------------------------------------------------------------------
# Composition table — NCM 3L conv (9 atomic layers) for both Li6 and Li5.4
# -----------------------------------------------------------------------------
COMPS = {
    'comp1':  {'se': 'comp1_slab_v2.xyz',            'ncm': 'ncm_7x7x1_3Lconv.xyz'},
    'comp2':  {'se': 'comp2_slab_v2.xyz',            'ncm': 'ncm_7x7x1_3Lconv.xyz'},
    'comp3':  {'se': 'comp3_slab_v1_PRESERVED.xyz',  'ncm': 'ncm_5x5x1_3Lconv.xyz'},
    'comp4':  {'se': 'comp4_slab_v1_PRESERVED.xyz',  'ncm': 'ncm_5x5x1_3Lconv.xyz'},
    'comp5':  {'se': 'comp5_slab_v1_PRESERVED.xyz',  'ncm': 'ncm_5x5x1_3Lconv.xyz'},
    'modelC': {'se': 'modelC_slab_v2_PRESERVED.xyz', 'ncm': 'ncm_5x5x1_3Lconv.xyz'},
}

# -----------------------------------------------------------------------------
# Parameters
# -----------------------------------------------------------------------------
GAP = 2.5            # Å, equilibrium SE/NCM separation (Camacho-Forero used 2.0-2.2; we keep 2.5 from v5)
VACUUM_TOP = 30.0    # Å, ISO slabs only (UMA OOD requires ≤30 Å vacuum)
LBFGS_FMAX = 0.03    # was 0.05 in v5; v9 hit 200 steps without converging at 0.05
LBFGS_STEPS = 400    # was 200 in v5

# NCM 3Lconv = 9 atomic layers. Fix middle 3 (layers 4-6, index 3-5).
NCM_FIX_LAYER_START = 3
NCM_FIX_LAYER_END = 6
NCM_TOTAL_LAYERS = 9

# Registry sampling (same as v5/v9: 6 high-sym + 30 random = 36 total)
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

RESULTS_DIR = Path("phase2a_v10_results"); RESULTS_DIR.mkdir(exist_ok=True)
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
    """ISO slabs only — adds vacuum on top so PBC z gives free top + bottom surfaces."""
    cell = atoms.cell.array.copy()
    cell[2, 2] += vac
    atoms.set_cell(cell, scale_atoms=False)
    atoms.set_pbc([True, True, True])
    return atoms


def fix_ncm_middle_layers(atoms, n_ncm,
                          layer_start=NCM_FIX_LAYER_START,
                          layer_end=NCM_FIX_LAYER_END,
                          total_layers=NCM_TOTAL_LAYERS):
    """Fix MIDDLE atomic layers of NCM (preserve bulk reference).

    For 3Lconv (9 atomic layers): fix layers [layer_start..layer_end) = [3..6) = layers 4,5,6.
    Bottom 3 layers and top 3 layers remain free → BOTH interfaces (direct and PBC)
    can express vacancy/cathode chemistry symmetrically.

    NCM is always indexed first (atoms 0..n_ncm) in stacked geometry.
    """
    ncm_z = atoms.positions[:n_ncm, 2]
    z_min, z_max = ncm_z.min(), ncm_z.max()
    z_thresh_lo = z_min + (z_max - z_min) * (layer_start / total_layers)
    z_thresh_hi = z_min + (z_max - z_min) * (layer_end / total_layers)
    fix_idx = [i for i in range(n_ncm)
               if z_thresh_lo <= atoms.positions[i, 2] <= z_thresh_hi]
    atoms.set_constraint(FixAtoms(indices=fix_idx))
    return len(fix_idx)


def stack_v10_sandwich(se, ncm, gap, shift_frac):
    """Sandwich stack: NCM | gap | SE | gap (via PBC z) → 2 interfaces.

    Final cell_z = z_extent + gap. PBC z connects SE_top to NCM_bottom across one gap.
    Result: NCM_top↔SE_bottom (direct interface) + SE_top↔NCM_bottom (PBC interface).
    """
    se_a = se.copy()
    ncm_a = ncm.copy()

    # 1. Lateral lattice match: SE laterally strained to NCM's a, b vectors
    new_se_cell = se_a.cell.array.copy()
    new_se_cell[0] = ncm_a.cell.array[0]
    new_se_cell[1] = ncm_a.cell.array[1]
    se_a.set_cell(new_se_cell, scale_atoms=True)

    # 2. xy-shift SE (registry sampling)
    dx, dy = shift_frac
    shift_cart = dx * ncm_a.cell.array[0] + dy * ncm_a.cell.array[1]
    se_a.translate([shift_cart[0], shift_cart[1], 0.0])
    se_a.wrap()

    # 3. Position: NCM_bottom at z=0, SE on top with `gap` separation
    ncm_a.translate([0, 0, -ncm_a.positions[:, 2].min()])
    ncm_z_max = ncm_a.positions[:, 2].max()
    se_z_min = se_a.positions[:, 2].min()
    se_a.translate([0, 0, ncm_z_max - se_z_min + gap])

    combined = ncm_a + se_a

    # 4. Sandwich cell z: z_extent + gap (PBC z creates 2nd interface)
    new_cell = ncm_a.cell.array.copy()
    z_extent = combined.positions[:, 2].max() - combined.positions[:, 2].min()
    new_cell[2] = [0.0, 0.0, z_extent + gap]
    combined.set_cell(new_cell, scale_atoms=False)
    combined.set_pbc([True, True, True])

    return combined, len(ncm_a)


def strained_se_iso(se, ncm):
    """Build SE iso slab strained to NCM lattice with vacuum (no FixAtoms)."""
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
    log("Phase 2a v10 — Sandwich Wad")
    log("Anchors: Camacho-Forero 2020 (slab method) + Komatsu 2022 (bulk thermo)")
    log(f"NCM: 3L conv (9 atomic layers, ~42.6 A); SE: paper #1 v2 anneal champion slabs")
    log(f"Sandwich: cell_z = z_extent + gap (no top vacuum)")
    log(f"FixAtoms: NCM middle 3 atomic layers; SE no FixAtoms")
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

    # -------------------------------------------------------------------------
    # Stage A — Iso slabs (NCM with FixAtoms middle 3L; SE no FixAtoms)
    # -------------------------------------------------------------------------
    log("=== Stage A: Iso slabs ===")
    ncm_done = set()
    for comp, paths in COMPS.items():
        if paths['ncm'] in ncm_done:
            continue
        if paths['ncm'] not in iso:
            ncm = read(paths['ncm'])
            ncm = add_vacuum(ncm, VACUUM_TOP)
            n_fix = fix_ncm_middle_layers(ncm, len(ncm))
            ncm.calc = calc
            log(f"  NCM {paths['ncm']}: n={len(ncm)}, "
                f"fix middle {n_fix} ({100*n_fix/len(ncm):.1f}%)")
            t0 = time.time()
            opt = LBFGS(ncm, logfile=None)
            opt.run(fmax=LBFGS_FMAX, steps=LBFGS_STEPS)
            E = float(ncm.get_potential_energy())
            iso[paths['ncm']] = {
                'E': E,
                'n': len(ncm),
                'type': 'NCM_iso_middle_fix_3L',
                'n_fixed': n_fix,
                'lbfgs_steps': opt.nsteps,
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
        # SE: no FixAtoms (Camacho-Forero standard)
        se_str.calc = calc
        log(f"  SE {comp}: n={len(se_str)}, no FixAtoms")
        t0 = time.time()
        opt = LBFGS(se_str, logfile=None)
        opt.run(fmax=LBFGS_FMAX, steps=LBFGS_STEPS)
        E = float(se_str.get_potential_energy())
        iso[key] = {
            'E': E,
            'n': len(se_str),
            'type': 'SE_iso_no_fix',
            'lbfgs_steps': opt.nsteps,
            'wall_min': (time.time() - t0) / 60,
        }
        write(str(RESULTS_DIR / f"iso_{comp}_SE_strained.xyz"), se_str)
        ISO_FILE.write_text(json.dumps(iso, indent=2))
        log(f"    -> E={E:.4f} ({(time.time()-t0)/60:.1f} min, steps={opt.nsteps})")

    # -------------------------------------------------------------------------
    # Stage B — Round-robin sandwich
    # -------------------------------------------------------------------------
    log(f"=== Stage B: SANDWICH @ d={GAP} A, NCM middle FixAtoms 3L, SE free ===")
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
                n_fix = fix_ncm_middle_layers(stacked, n_ncm)
                stacked.calc = calc
                opt = LBFGS(stacked, logfile=None)
                opt.run(fmax=LBFGS_FMAX, steps=LBFGS_STEPS)
                E_int = float(stacked.get_potential_energy())
                steps = opt.nsteps
                write(str(xyz_relaxed), stacked)

                # Wad calculation: SANDWICH /(2A)
                A = xy_area(stacked.cell.array)
                E_se = iso[f"{comp}_SE_strained"]['E']
                E_ncm = iso[cd['paths']['ncm']]['E']
                Wad = (E_se + E_ncm - E_int) / (2 * A) * 16.0218

                # Diagnostic only (NOT used to filter): Li migration into NCM
                syms = stacked.get_chemical_symbols()
                ncm_z_max = float(stacked.positions[:n_ncm, 2].max())
                cell_z = float(stacked.cell.array[2, 2])
                # Top interface (direct): SE Li penetrated below NCM_top
                li_mig_top = sum(1 for i in range(n_ncm, len(stacked))
                                 if syms[i] == 'Li'
                                 and stacked.positions[i, 2] < ncm_z_max - 1.0)
                # PBC interface: SE Li above (cell_z - 1.0) → entered via PBC
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
                    'n_fixed': n_fix,
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

    log(f"=== Phase 2a v10 DONE: {done}/{total} in "
        f"{(time.time()-t_start)/3600:.1f}h ===")


if __name__ == "__main__":
    main()
