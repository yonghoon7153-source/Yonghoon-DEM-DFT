"""run_comp4_v2_zshift_champion.py — comp4 v2 anneal champion z-shift scan.

Strategy:
  Comp4_v2 has Cl-exposed surface anomaly at z=0 (anneal champion termination).
  Other z-shifts may expose Li/S surfaces (no Cl anomaly), giving Wad more
  representative of Li5.4 family with normal halogen distribution.

Procedure:
  1. Run full 5z × 36 reg × 16 gap ensemble for comp4_v2 (~20 min)
  2. For each of 5 z-shifts, analyze the SE-bottom surface (which faces NCM)
     and count exposed Li/Cl/Br/S atoms within 2 Å of interface-facing layer
  3. Identify z* with LEAST Cl exposed → 'normal' Li5.4 surface
  4. Apply eiso-fix correction (same ΔWad_strain = need fresh E_ncm in SE cell)
  5. Output per-z and best-z summary: Wad curves, surface composition

Run on gabia:
  cd /data/work/v30u_ensemble
  python3 run_comp4_v2_zshift_champion.py
"""
import os, sys, json, time, gc
from pathlib import Path
import numpy as np
from ase.io import read

COMP = 'comp4'
SE_FILE  = 'comp4_slab_v2_PRESERVED.xyz'   # anneal champion (v2)
NCM_FILE = 'ncm_5x5x1_PRESERVED.xyz'

D_VALUES = [0.6, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0, 2.2, 2.5, 2.8, 3.0, 3.5, 4.0, 5.0, 7.0]

HIGH_SYM = [
    ("R1_origin",   (0.0, 0.0)),
    ("R2_half_x",   (0.5, 0.0)),
    ("R3_half_y",   (0.0, 0.5)),
    ("R4_diagonal", (0.5, 0.5)),
    ("R5_hex1",     (1/3, 2/3)),
    ("R6_hex2",     (2/3, 1/3)),
]
N_RANDOM = 30
RANDOM_SEED = 42
VACUUM_TOP = 30.0
N_ZSHIFTS = 5

SURFACE_DEPTH = 2.0    # Å — count atoms within this of SE-bottom (NCM-facing face)

WORK = Path('/data/work/v30u_ensemble')
OUT  = WORK / 'comp4_v2_zshift_champion_results'
OUT.mkdir(exist_ok=True)
LOG = OUT / 'progress.log'


def log(msg):
    s = f"[{time.strftime('%H:%M:%S')}] {msg}"
    print(s, flush=True)
    with open(LOG, 'a') as f:
        f.write(s + "\n")


# ─── verbatim from run_v30u_1L_correct.py ───────────────────────────────────

def add_vacuum(atoms, vac):
    cell = atoms.cell.array.copy()
    cell[2, 2] += vac
    atoms.set_cell(cell, scale_atoms=False)
    atoms.set_pbc([True, True, True])
    return atoms


def stack_interface(se, ncm, gap, shift_frac):
    se_a = se.copy(); ncm_a = ncm.copy()
    dx, dy = shift_frac
    shift_cart = dx * ncm_a.cell.array[0] + dy * ncm_a.cell.array[1]
    ncm_a.translate([shift_cart[0], shift_cart[1], 0])
    ncm_a.wrap()
    ncm_a.translate([0, 0, -ncm_a.positions[:, 2].min()])
    ncm_z_max = ncm_a.positions[:, 2].max()
    se_z_min  = se_a.positions[:, 2].min()
    se_a.translate([0, 0, ncm_z_max - se_z_min + gap])
    combined = ncm_a + se_a
    new_cell = se.cell.array.copy()
    z_extent = combined.positions[:, 2].max() - combined.positions[:, 2].min()
    new_cell[2] = [0, 0, z_extent + VACUUM_TOP]
    combined.set_cell(new_cell, scale_atoms=False)
    combined.set_pbc([True, True, True])
    return combined


def zshift_variant(atoms, frac):
    a = atoms.copy()
    cz = a.cell.lengths()[2]
    pos = a.positions.copy()
    pos[:, 2] = (pos[:, 2] + frac * cz) % cz
    a.set_positions(pos)
    return a


def xy_area(cell):
    a1 = cell[0]; a2 = cell[1]
    cross = np.cross(a1[:2].tolist() + [0], a2[:2].tolist() + [0])
    return float(np.linalg.norm(cross))


def ncm_in_se_cell(se, ncm):
    """E_ncm reference in SE cell (eiso_fix consistent)."""
    ncm_a = ncm.copy()
    ncm_a.wrap()
    ncm_a.translate([0, 0, -ncm_a.positions[:, 2].min()])
    z_extent = ncm_a.positions[:, 2].max() - ncm_a.positions[:, 2].min()
    new_cell = se.cell.array.copy()
    new_cell[2] = [0, 0, z_extent + VACUUM_TOP]
    ncm_a.set_cell(new_cell, scale_atoms=False)
    ncm_a.set_pbc([True, True, True])
    return ncm_a


def surface_composition(se_zshifted):
    """For a z-shifted SE slab, count atoms within SURFACE_DEPTH of z_min.
    (z_min = bottom of SE in lab frame = the face that meets NCM after stack)."""
    pos = se_zshifted.positions
    syms = se_zshifted.get_chemical_symbols()
    z_min = pos[:, 2].min()
    mask = pos[:, 2] <= (z_min + SURFACE_DEPTH)
    counts = {}
    for s, m in zip(syms, mask):
        if m:
            counts[s] = counts.get(s, 0) + 1
    counts['total'] = int(mask.sum())
    return counts


# ─── UMA ────────────────────────────────────────────────────────────────────

_predictor = None


def make_calc():
    global _predictor
    from fairchem.core import pretrained_mlip
    from fairchem.core.calculate.ase_calculator import FAIRChemCalculator
    if _predictor is None:
        _predictor = pretrained_mlip.get_predict_unit("uma-s-1p1", device="cuda")
    return FAIRChemCalculator(_predictor, task_name="omat")


# ─── MAIN ───────────────────────────────────────────────────────────────────

def main():
    # build registry list (same seed as run_v30u_1L_correct.py)
    rng = np.random.default_rng(RANDOM_SEED)
    RANDOM_REG = [(f"rand_{i+1:03d}", (rng.uniform(0, 1), rng.uniform(0, 1)))
                  for i in range(N_RANDOM)]
    ALL_REG = HIGH_SYM + RANDOM_REG

    log("=" * 70)
    log(f"comp4_v2 anneal champion z-shift scan")
    log(f"  SE  = {SE_FILE}  |  NCM = {NCM_FILE}")
    log(f"  N_ZSHIFTS={N_ZSHIFTS}  registries={len(ALL_REG)}  gaps={len(D_VALUES)}")
    log("=" * 70)

    se_base = read(WORK / SE_FILE)
    ncm     = read(WORK / NCM_FILE)
    log(f"SE atoms: {len(se_base)}  |  NCM atoms: {len(ncm)}")

    # ─── Surface composition analysis per z-shift ───────────────────────────
    log("\n── Per-z surface composition (SE face that meets NCM) ──")
    z_compositions = {}
    for iz in range(N_ZSHIFTS):
        se_z = zshift_variant(se_base, iz / N_ZSHIFTS)
        comp = surface_composition(se_z)
        z_compositions[iz] = comp
        n_total = comp.get('total', 0)
        n_li = comp.get('Li', 0)
        n_cl = comp.get('Cl', 0)
        n_br = comp.get('Br', 0)
        n_s  = comp.get('S',  0)
        log(f"  z{iz}: total={n_total}  Li={n_li}  S={n_s}  "
            f"Cl={n_cl}  Br={n_br}  (within {SURFACE_DEPTH}Å of bottom face)")

    # Identify least-Cl z(s)
    z_by_cl = sorted(range(N_ZSHIFTS),
                     key=lambda iz: z_compositions[iz].get('Cl', 0))
    log(f"\n  → z order by Cl exposure (ascending): {z_by_cl}")
    log(f"  → candidate non-Cl-exposed z: z{z_by_cl[0]} "
        f"(Cl={z_compositions[z_by_cl[0]].get('Cl', 0)})")

    # ─── Compute E_iso (z=0 SE iso + NCM iso in SE cell, eiso_fix style) ────
    log("\n── Loading UMA-s-1p1 ──")
    calc = make_calc()

    log("\n── E_iso references ──")
    # Per-z E_se_iso
    E_se_per_z = []
    for iz in range(N_ZSHIFTS):
        se_z = zshift_variant(se_base, iz / N_ZSHIFTS)
        se_z_vac = add_vacuum(se_z, VACUUM_TOP)
        se_z_vac.calc = calc
        E_se = float(se_z_vac.get_potential_energy())
        E_se_per_z.append(E_se)
        log(f"  E_se_iso z{iz} = {E_se:.4f} eV")

    # E_ncm_iso in SE cell (eiso_fix)
    ncm_in_se = ncm_in_se_cell(se_base, ncm)
    ncm_in_se.calc = calc
    E_ncm_iso = float(ncm_in_se.get_potential_energy())
    log(f"  E_ncm_iso (SE cell, eiso_fix) = {E_ncm_iso:.4f} eV")

    # ─── Ensemble loop ───────────────────────────────────────────────────────
    n_configs = N_ZSHIFTS * len(ALL_REG)
    idx = 0
    t_start = time.time()

    comp_data = {
        'comp':            COMP + '_v2',
        'se_file':         SE_FILE,
        'ncm_file':        NCM_FILE,
        'gaps':            D_VALUES,
        'registries':      [r[0] for r in ALL_REG],
        'n_zshifts':       N_ZSHIFTS,
        'E_se_iso_per_z':  E_se_per_z,
        'E_ncm_iso':       E_ncm_iso,        # SE cell (eiso_fix consistent)
        'z_surface_comp':  z_compositions,
        'Wad_per_z_per_reg': {f"z{iz}": {} for iz in range(N_ZSHIFTS)},
        'Wad_samples':       {f"{g:.3f}": [] for g in D_VALUES},
        'Wad_samples_per_z': {f"z{iz}": {f"{g:.3f}": [] for g in D_VALUES}
                              for iz in range(N_ZSHIFTS)},
    }

    for iz in range(N_ZSHIFTS):
        se_z = zshift_variant(se_base, iz / N_ZSHIFTS)
        E_se = E_se_per_z[iz]
        for reg_name, shift in ALL_REG:
            idx += 1
            reg_data = {'shift': list(shift), 'curve': {}}
            for d in D_VALUES:
                d_key = f"{d:.3f}"
                try:
                    stacked = stack_interface(se_z, ncm, d, shift)
                    stacked.calc = calc
                    E_int = float(stacked.get_potential_energy())
                    A = float(xy_area(stacked.cell.array))
                    Wad = -(E_int - E_se - E_ncm_iso) / A * 16.0218
                    reg_data['curve'][d_key] = {
                        'E_int': E_int, 'Wad_J_per_m2': Wad, 'area_A2': A,
                    }
                    comp_data['Wad_samples'][d_key].append(Wad)
                    comp_data['Wad_samples_per_z'][f"z{iz}"][d_key].append(Wad)
                except Exception as e:
                    log(f"  FAIL z{iz} {reg_name} d={d:.2f}: {e}")
                    reg_data['curve'][d_key] = {'E_int': None, 'error': str(e)}

            comp_data['Wad_per_z_per_reg'][f"z{iz}"][reg_name] = reg_data
            if idx % 10 == 0 or idx == n_configs:
                el = time.time() - t_start
                eta = el * (n_configs - idx) / idx
                log(f"  config {idx}/{n_configs}  z{iz} {reg_name}  "
                    f"el={el/60:.1f}min ETA={eta/60:.1f}min")
            gc.collect()

    # ─── Per-z mean Wad curves ──────────────────────────────────────────────
    comp_data['Wad_mean_per_z'] = {}
    comp_data['Wad_well_per_z'] = {}
    log("\n── Per-z Wad summary (36-reg mean) ──")
    for iz in range(N_ZSHIFTS):
        means = []
        for d in D_VALUES:
            dk = f"{d:.3f}"
            samples = comp_data['Wad_samples_per_z'][f"z{iz}"][dk]
            means.append(float(np.mean(samples)) if samples else None)
        comp_data['Wad_mean_per_z'][f"z{iz}"] = means
        valid = [m for m in means if m is not None]
        if valid:
            wad_max = max(valid)
            asymp = means[-1] if means[-1] is not None else None
            cl_at_surf = z_compositions[iz].get('Cl', 0)
            comp_data['Wad_well_per_z'][f"z{iz}"] = wad_max
            log(f"  z{iz}: Cl_surf={cl_at_surf}  Wad_well={wad_max:+.4f}  "
                f"asymp={asymp:+.4f}")

    # ─── Aggregate over all 5z × 36 reg (= consistent with v30u_1L_correct) ──
    comp_data['Wad_mean'] = []
    comp_data['Wad_std']  = []
    for d in D_VALUES:
        dk = f"{d:.3f}"
        samples = comp_data['Wad_samples'][dk]
        comp_data['Wad_mean'].append(float(np.mean(samples)) if samples else None)
        comp_data['Wad_std'].append(float(np.std(samples)) if samples else None)

    log(f"\n5z × 36-reg overall mean Wad_well = {max(m for m in comp_data['Wad_mean'] if m is not None):+.4f}")
    log(f"5z × 36-reg overall asymp        = {comp_data['Wad_mean'][-1]:+.4f}")

    # ─── Save ────────────────────────────────────────────────────────────────
    json.dump(comp_data, open(OUT / 'comp4_v2_done.json', 'w'), indent=2)
    log(f"\nSaved: {OUT}/comp4_v2_done.json")

    log("\n" + "=" * 70)
    log("INTERPRETATION:")
    log("  Compare Wad_well_per_z[zN] vs paper exp:")
    log("    comp3 paper = 316 aJ  (between us → comp4 paper = 298 aJ → comp5 = 249)")
    log(f"  Use z* with smallest Cl_surf as comp4_v2 representative.")
    log(f"  Likely candidate: z{z_by_cl[0]} (Cl_surf={z_compositions[z_by_cl[0]].get('Cl', 0)})")
    log(f"  Compare its Wad to current v1 result (Wad_well_fixed = +1.004 J/m²)")
    log("=" * 70)


if __name__ == "__main__":
    main()
