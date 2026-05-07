"""Phase 2a v11 — Haruyama 2014 faithful single interface + UMA stability.

Based on lessons from:
- v9 cleavage: rigid sep → cross-family inverted ❌
- v10 sandwich: SE no fix → Li intermixing dominates → cross-family inverted ❌
- v10b sandwich + SE-fix: same inversion (cycle 1: comp1=1.96, comp3=+0.22, comp4=-0.28) ❌
- Lesson (Haruyama 2014 Section 2.1, EXPLICIT): "the presence of the vacuum
  region is quite crucial. Without this vacuum, the supercell approach always
  involves two interfaces, which are atomically different in most cases."
- Conclusion: SANDWICH IS WRONG for oxide/sulfide hetero (LPSCl/NCM is exact match
  to Haruyama's anti-sandwich case). Must use SINGLE interface + vacuum.

References (필독/literature/):
- ⭐ Haruyama et al., Chem. Mater. 26, 4248 (2014) — DOI 10.1021/cm5016959
    PRIMARY method anchor. DFT+U slab for LCO/β-Li3PS4 ± LiNbO3 buffer.
    Section 2.1: explicit anti-sandwich for asymmetric heterointerfaces.
    Section 3.4: SCL mechanism — Li from LPS subsurface adsorbs on LCO surface
    → vacancy chemical anchor narrative for paper #2.
    Reference value: LCO/LPS Wad = 4.3 eV/nm² = 0.69 J/m².
- Komatsu et al., JPCC 126, 17482 (2022) — bulk thermo anchor:
    LiNiO2/LPSCl ΔED = -424 meV/atom (most reactive NCM).
- Camacho-Forero & Balbuena, Chem. Mater. 32, 360 (2020) — sulfide-cathode
    AIMD reaction taxonomy (use as secondary reference for chemistry observed).

v11 method elements (= Haruyama 2014 + UMA stability hack):
1. SINGLE interface + vacuum 30 Å on top (Haruyama 2014 §2.1 explicit)
2. Wad = (E_iso_NCM + E_iso_SE − E_int) / A  (Haruyama definition, single interface)
3. NCM 3L conv (9 atomic layers, 42.57 Å) — proper structure (1L is broken per user)
4. FixAtoms strategy:
     - NCM bottom 1/3 (3 atomic layers, ~14 Å) — bulk reference + prevent PBC vacuum drift
     - SE top 1/3 (~33% by z) — bulk reference + prevent vacuum drift
     - Both NCM_top + SE_bottom (interface region) FREE → vacancy chemistry can develop
   (Haruyama himself uses NO FixAtoms because VASP DFT doesn't suffer UMA-OOD-at-vacuum)
5. LBFGS fmax=0.05, steps=300
6. Iso slabs: same FixAtoms strategy (consistency between iso and interface reference)
7. 36 reg sampling (6 high-sym + 30 random) × 6 comps round-robin

Active interface chemistry zone:
   NCM_top (atomic layers 7-9, FREE) ↔ SE_bottom (atomic layers 1-3, FREE)
   ↳ Vacancy in Li5.4 SE bottom can develop chemical anchor with NCM-O surface

Expected paper-target ranges (these are EXPECTATIONS, not validated):
- comp1/2 (Li6): 0.5-1.5 J/m² (Haruyama LCO/LPS anchor 0.69, our LiNiO2 should be slightly higher)
- comp3-5/modelC (Li5.4): expected > Li6 if vacancy chemical anchor mechanism is real
- Cross-family Li5.4 > Li6 = vacancy chemical anchor mechanism validation

CODE_INVENTORY F4: ❓ UNKNOWN — to be validated by pilot.
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
VACUUM_TOP = 30.0     # Å (Haruyama uses 15 Å; we use 30 Å for UMA OOD safety)
LBFGS_FMAX = 0.05
LBFGS_STEPS = 300

LO_FRAC = 1.0 / 3.0   # NCM bottom 1/3 (z_min..z_min + 1/3 range)
HI_FRAC = 2.0 / 3.0   # SE top 1/3 (z_min + 2/3 range..z_max)

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

RESULTS_DIR = Path("phase2a_v11_results"); RESULTS_DIR.mkdir(exist_ok=True)
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
    """Add vacuum on top of the slab (z direction)."""
    cell = atoms.cell.array.copy()
    cell[2, 2] += vac
    atoms.set_cell(cell, scale_atoms=False)
    atoms.set_pbc([True, True, True])
    return atoms


def find_bottom_third(atoms, idx_start, idx_end, lo_frac=LO_FRAC):
    """Indices in [idx_start, idx_end) with z in BOTTOM lo_frac of that group's z range."""
    z = atoms.positions[idx_start:idx_end, 2]
    if len(z) == 0:
        return []
    z_min, z_max = z.min(), z.max()
    z_thresh = z_min + (z_max - z_min) * lo_frac
    return [i for i in range(idx_start, idx_end)
            if atoms.positions[i, 2] <= z_thresh]


def find_top_third(atoms, idx_start, idx_end, hi_frac=HI_FRAC):
    """Indices in [idx_start, idx_end) with z in TOP (1 - hi_frac) of that group's z range."""
    z = atoms.positions[idx_start:idx_end, 2]
    if len(z) == 0:
        return []
    z_min, z_max = z.min(), z.max()
    z_thresh = z_min + (z_max - z_min) * hi_frac
    return [i for i in range(idx_start, idx_end)
            if atoms.positions[i, 2] >= z_thresh]


def fix_iso_ncm(ncm):
    """NCM iso (with vacuum on top): fix BOTTOM 1/3 (PBC vacuum side, bulk reference)."""
    idx = find_bottom_third(ncm, 0, len(ncm))
    ncm.set_constraint(FixAtoms(indices=idx))
    return len(idx)


def fix_iso_se(se):
    """SE iso (with vacuum on top): fix TOP 1/3 (vacuum-facing side, bulk reference).

    Mirror of NCM iso: in interface, NCM bottom faces PBC vacuum, SE top faces
    direct vacuum. So both sides closest to vacuum get fixed for UMA stability.
    """
    idx = find_top_third(se, 0, len(se))
    se.set_constraint(FixAtoms(indices=idx))
    return len(idx)


def fix_v11_interface(stacked, n_ncm):
    """Stacked interface (NCM bottom, SE top, vacuum on top of SE):
       - NCM bottom 1/3: prevents PBC vacuum drift + bulk reference
       - SE top 1/3:    prevents direct vacuum drift + bulk reference
       - NCM top + SE bottom (interface region) FREE → vacancy chemistry develops
    """
    ncm_idx = find_bottom_third(stacked, 0, n_ncm)
    se_idx = find_top_third(stacked, n_ncm, len(stacked))
    stacked.set_constraint(FixAtoms(indices=ncm_idx + se_idx))
    return len(ncm_idx) + len(se_idx), len(ncm_idx), len(se_idx)


def stack_v11_single_interface(se, ncm, gap, shift_frac):
    """Single interface (Haruyama 2014 §2.1 — vacuum is CRUCIAL):
       Cell layout: NCM bottom → gap → SE top → vacuum 30 Å → cell_z (PBC)
       cell_z = z_extent + VACUUM_TOP (NOT + gap)
       PBC z connects vacuum-end back to NCM bottom (effectively NCM bottom faces vacuum too)
    """
    se_a = se.copy()
    ncm_a = ncm.copy()

    # 1. Lateral lattice match: SE strained to NCM (high modulus, Haruyama protocol)
    new_se_cell = se_a.cell.array.copy()
    new_se_cell[0] = ncm_a.cell.array[0]
    new_se_cell[1] = ncm_a.cell.array[1]
    se_a.set_cell(new_se_cell, scale_atoms=True)

    # 2. xy-shift SE (Haruyama §2.1 systematic lateral slide → 16/4/9 samples;
    #    we use 36 = 6 high-sym + 30 random for denser sampling)
    dx, dy = shift_frac
    shift_cart = dx * ncm_a.cell.array[0] + dy * ncm_a.cell.array[1]
    se_a.translate([shift_cart[0], shift_cart[1], 0.0])
    se_a.wrap()

    # 3. Position: NCM bottom at z=0, SE on top with `gap` separation
    ncm_a.translate([0, 0, -ncm_a.positions[:, 2].min()])
    ncm_z_max = ncm_a.positions[:, 2].max()
    se_z_min = se_a.positions[:, 2].min()
    se_a.translate([0, 0, ncm_z_max - se_z_min + gap])

    combined = ncm_a + se_a

    # 4. ⭐ KEY DIFFERENCE FROM v10/v10b SANDWICH:
    #    cell_z = z_extent + VACUUM_TOP (30 Å vacuum on top, Haruyama §2.1)
    #    NOT cell_z = z_extent + gap (sandwich, predicts asymmetric polarization → wrong)
    new_cell = ncm_a.cell.array.copy()
    z_extent = combined.positions[:, 2].max() - combined.positions[:, 2].min()
    new_cell[2] = [0.0, 0.0, z_extent + VACUUM_TOP]
    combined.set_cell(new_cell, scale_atoms=False)
    combined.set_pbc([True, True, True])

    return combined, len(ncm_a)


def strained_se_iso(se, ncm):
    """SE iso with vacuum (FixAtoms applied separately by fix_iso_se)."""
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
    log("Phase 2a v11 — Haruyama 2014 single interface + UMA stability hack")
    log("Anchors:")
    log("  PRIMARY:  Haruyama 2014 (LCO/LPS DFT+U slab, anti-sandwich for hetero)")
    log("  BULK:     Komatsu 2022 (LiNiO2/LPSCl ΔED = -424 meV/atom)")
    log("  CHEMISTRY: Camacho-Forero 2020 (sulfide-cathode AIMD reaction taxonomy)")
    log("Method:")
    log("  Geometry: SINGLE interface + vacuum 30 Å (Haruyama §2.1 explicit)")
    log("  Wad = (E_iso_NCM + E_iso_SE - E_int) / A   [single interface, /A]")
    log("  FixAtoms: NCM bottom 1/3 + SE top 1/3 (vacuum-touching sides)")
    log("            Active interface NCM_top + SE_bottom both FREE")
    log(f"  LBFGS fmax={LBFGS_FMAX}, steps={LBFGS_STEPS}, gap={GAP} A, vacuum={VACUUM_TOP} A")
    log(f"  Round-robin: {len(COMPS)} comps x {len(ALL_REG)} regs = "
        f"{len(COMPS)*len(ALL_REG)} interfaces")
    log(f"CUDA_VISIBLE_DEVICES={os.environ.get('CUDA_VISIBLE_DEVICES')}")
    log("=" * 70)

    log("Loading UMA...")
    calc = make_calc()
    log("UMA loaded.")

    results = json.loads(RESULT_FILE.read_text()) if RESULT_FILE.exists() else {}
    iso = json.loads(ISO_FILE.read_text()) if ISO_FILE.exists() else {}

    # -------------------------------------------------------------------------
    # Stage A — Iso slabs
    #   NCM iso: vacuum 30 Å, fix BOTTOM 1/3 (PBC vacuum side)
    #   SE iso:  vacuum 30 Å, fix TOP 1/3 (direct vacuum side)
    # -------------------------------------------------------------------------
    log("=== Stage A: Iso slabs (NCM bottom 1/3 fix + SE top 1/3 fix) ===")
    ncm_done = set()
    for comp, paths in COMPS.items():
        if paths['ncm'] in ncm_done:
            continue
        if paths['ncm'] not in iso:
            ncm = read(paths['ncm'])
            ncm = add_vacuum(ncm, VACUUM_TOP)
            n_fix = fix_iso_ncm(ncm)
            ncm.calc = calc
            log(f"  NCM {paths['ncm']}: n={len(ncm)}, "
                f"fix bottom 1/3 = {n_fix} ({100*n_fix/len(ncm):.1f}%)")
            t0 = time.time()
            opt = LBFGS(ncm, logfile=None)
            opt.run(fmax=LBFGS_FMAX, steps=LBFGS_STEPS)
            E = float(ncm.get_potential_energy())
            iso[paths['ncm']] = {
                'E': E, 'n': len(ncm), 'type': 'NCM_iso_bottom_1_3_fix',
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
        n_fix = fix_iso_se(se_str)
        se_str.calc = calc
        log(f"  SE {comp}: n={len(se_str)}, "
            f"fix top 1/3 = {n_fix} ({100*n_fix/len(se_str):.1f}%)")
        t0 = time.time()
        opt = LBFGS(se_str, logfile=None)
        opt.run(fmax=LBFGS_FMAX, steps=LBFGS_STEPS)
        E = float(se_str.get_potential_energy())
        iso[key] = {
            'E': E, 'n': len(se_str), 'type': 'SE_iso_top_1_3_fix',
            'n_fixed': n_fix, 'lbfgs_steps': opt.nsteps,
            'wall_min': (time.time() - t0) / 60,
        }
        write(str(RESULTS_DIR / f"iso_{comp}_SE_strained.xyz"), se_str)
        ISO_FILE.write_text(json.dumps(iso, indent=2))
        log(f"    -> E={E:.4f} ({(time.time()-t0)/60:.1f} min, steps={opt.nsteps})")

    # -------------------------------------------------------------------------
    # Stage B — Round-robin single interface
    # -------------------------------------------------------------------------
    log(f"=== Stage B: SINGLE interface @ d={GAP} A, NCM bot 1/3 + SE top 1/3 fix ===")
    log("Active interface: NCM_top (free) <-> SE_bottom (free) — chemistry develops here")
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
                stacked, n_ncm = stack_v11_single_interface(
                    cd['se'], cd['ncm'], GAP, shift)
                n_fix_total, n_fix_ncm, n_fix_se = fix_v11_interface(stacked, n_ncm)
                stacked.calc = calc
                opt = LBFGS(stacked, logfile=None)
                opt.run(fmax=LBFGS_FMAX, steps=LBFGS_STEPS)
                E_int = float(stacked.get_potential_energy())
                steps = opt.nsteps
                write(str(xyz_relaxed), stacked)

                # Wad = (E_iso_NCM + E_iso_SE - E_int) / A   [Haruyama, single interface]
                A = xy_area(stacked.cell.array)
                E_se = iso[f"{comp}_SE_strained"]['E']
                E_ncm = iso[cd['paths']['ncm']]['E']
                Wad = (E_se + E_ncm - E_int) / A * 16.0218

                # Diagnostic Li migration: only one interface (top NCM <-> bottom SE)
                syms = stacked.get_chemical_symbols()
                ncm_z_max = float(stacked.positions[:n_ncm, 2].max())
                cell_z = float(stacked.cell.array[2, 2])
                # SE Li penetrated below NCM_top (= migrated INTO NCM region)
                li_mig_iface = sum(1 for i in range(n_ncm, len(stacked))
                                   if syms[i] == 'Li'
                                   and stacked.positions[i, 2] < ncm_z_max - 1.0)

                results[comp][reg_name] = {
                    'shift': list(shift),
                    'E_int': E_int, 'E_se_iso': E_se, 'E_ncm_iso': E_ncm,
                    'Wad_J_per_m2': Wad,
                    'A_A2': A, 'n_atoms': len(stacked),
                    'n_fixed': n_fix_total, 'n_fix_ncm': n_fix_ncm, 'n_fix_se': n_fix_se,
                    'cell_z_A': cell_z, 'lbfgs_steps': steps,
                    'li_mig_iface': li_mig_iface,
                    'wall_min': (time.time() - t0) / 60,
                }
                done += 1
                eta = (time.time() - t_start) / done * (total - done)
                wln = f" Li_mig={li_mig_iface}" if li_mig_iface > 0 else ""
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

    log(f"=== Phase 2a v11 DONE: {done}/{total} in {(time.time()-t_start)/3600:.1f}h ===")


if __name__ == "__main__":
    main()
