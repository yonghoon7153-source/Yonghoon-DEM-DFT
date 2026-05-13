"""run_v30u_1L_face_flip.py — physical face-flip test (no PBC wrap).

Question: 5z-shift PBC wrap is unphysical (cuts bonds at arbitrary z).
A clean way to expose 'different face' to NCM is to MIRROR the SE slab
in the xy plane — this is a proper symmetry operation that:
  • Preserves crystal space group
  • Brings the original top face to the bottom (NCM-facing) position
  • Introduces no broken bonds or wrap artifacts
  • Represents a real alternative cleave / particle orientation

Procedure (z=0, no z-shift):
  1. For each comp, build TWO SE variants:
       face_A: original SE
       face_B: flipped (z_new = z_max + z_min - z_old)
  2. For each face × 36 registries × 16 gaps → rigid Wad
  3. Compare Wad curves face A vs face B
       - Symmetric slab → Wad_A ≈ Wad_B
       - Asymmetric slab → Wad differs (one face binds more strongly)

If flip gives substantially different Wad and the family ordering
flips toward paper direction → SE slab asymmetry is a significant
factor in our previous comparison.

Cost:  4 comp × 2 face × 36 reg × 16 gap = 4608 SCFs ≈ ~40 min
       + 4 × 2 E_se_iso SCFs

Run on gabia:
  cd /data/work/v30u_ensemble
  nohup python3 run_v30u_1L_face_flip.py > face_flip.log 2>&1 &
"""
import os, sys, json, time, gc
from pathlib import Path
import numpy as np
from ase.io import read, write

COMPS = {
    'comp1':    {'se': 'comp1_slab_v2.xyz',            'ncm': 'ncm_7x7x1_PRESERVED.xyz', 'family': 'Li6'},
    'comp2':    {'se': 'comp2_slab_v2.xyz',            'ncm': 'ncm_7x7x1_PRESERVED.xyz', 'family': 'Li6'},
    'comp4_v1': {'se': 'comp4_slab_v1_PRESERVED.xyz',  'ncm': 'ncm_5x5x1_PRESERVED.xyz', 'family': 'Li5.4'},
    'comp4_v2': {'se': 'comp4_slab_v2_PRESERVED.xyz',  'ncm': 'ncm_5x5x1_PRESERVED.xyz', 'family': 'Li5.4'},
    'modelC':   {'se': 'modelC_slab_v2_PRESERVED.xyz', 'ncm': 'ncm_5x5x1_PRESERVED.xyz', 'family': 'Li5.4'},
}
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

WORK    = Path('/data/work/v30u_ensemble')
ISO_REF = WORK / 'v30u_1L_correct_results_eiso_fix'
OUT     = WORK / 'face_flip_results'
OUT.mkdir(exist_ok=True)
SLAB_OUT = OUT / 'slabs'
SLAB_OUT.mkdir(exist_ok=True)
LOG = OUT / 'progress.log'


def log(msg):
    s = f"[{time.strftime('%H:%M:%S')}] {msg}"
    print(s, flush=True)
    with open(LOG, 'a') as f:
        f.write(s + "\n")


# ─── physical face flip ─────────────────────────────────────────────────────

def flip_se_xy_plane(se):
    """Mirror SE in the xy plane (z → z_top + z_bottom − z).
    Brings the original top face to the NCM-contact position. No PBC wrap,
    no atom shuffling — just one symmetry operation. Preserves cell, atom
    types, intra-atomic bonds, and crystal space group."""
    a = se.copy()
    pos = a.positions.copy()
    z_top    = pos[:, 2].max()
    z_bottom = pos[:, 2].min()
    pos[:, 2] = z_top + z_bottom - pos[:, 2]
    a.set_positions(pos)
    return a


# ─── verbatim phase1 geometry ───────────────────────────────────────────────

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


def add_vacuum(atoms, vac):
    cell = atoms.cell.array.copy()
    cell[2, 2] += vac
    atoms.set_cell(cell, scale_atoms=False)
    atoms.set_pbc([True, True, True])
    return atoms


def xy_area(cell):
    a1 = cell[0]; a2 = cell[1]
    cross = np.cross(a1[:2].tolist() + [0], a2[:2].tolist() + [0])
    return float(np.linalg.norm(cross))


def surface_composition(se, depth=2.0):
    """Count atoms within `depth` Å of SE-bottom face (NCM-facing)."""
    pos = se.positions
    syms = se.get_chemical_symbols()
    z_min = pos[:, 2].min()
    mask = pos[:, 2] <= (z_min + depth)
    cnt = {}
    for s, m in zip(syms, mask):
        if m: cnt[s] = cnt.get(s, 0) + 1
    cnt['total'] = int(mask.sum())
    return cnt


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
    rng = np.random.default_rng(RANDOM_SEED)
    RANDOM_REG = [(f"rand_{i+1:03d}", (rng.uniform(0, 1), rng.uniform(0, 1)))
                  for i in range(N_RANDOM)]
    ALL_REG = HIGH_SYM + RANDOM_REG

    # filter out comps where SE xyz file doesn't exist on disk
    avail = {c: info for c, info in COMPS.items() if (WORK / info['se']).exists()}
    n_total = len(avail) * 2 * len(ALL_REG) * len(D_VALUES)
    log("=" * 70)
    log(f"Physical face-flip test (z=0, no PBC wrap)")
    log(f"  comps={list(avail.keys())} × faces=2 × reg={len(ALL_REG)} × gaps={len(D_VALUES)} "
        f"= {n_total} SCFs (~{n_total*0.5/60:.0f} min)")
    log("=" * 70)

    log("\nLoading UMA-s-1p1...")
    calc = make_calc()
    log("UMA loaded.\n")

    t_global = time.time()
    summary = {}
    idx = 0

    for c, info in avail.items():
        # comp4_v1 / comp4_v2 share the same E_ncm reference (same NCM 5x5x1).
        # Use comp4's eiso fix JSON if available, fall back to any v1 form.
        iso_key = c.replace('_v1', '').replace('_v2', '')
        f_iso = ISO_REF / f"{iso_key}_done.json"
        if not f_iso.exists():
            log(f"[{c}] missing eiso JSON ({f_iso.name}), skip"); continue
        d_iso = json.load(open(f_iso))
        E_ncm_iso = d_iso['E_ncm_iso']

        log(f"\n========= {c} (family {info['family']}) =========")
        se_base = read(WORK / info['se'])
        ncm     = read(WORK / info['ncm'])

        se_A = se_base.copy()                 # face A (NCM-facing = original bottom)
        se_B = flip_se_xy_plane(se_base)      # face B (NCM-facing = original top)

        # Save inspection xyzs
        write(SLAB_OUT / f"{c}_faceA.xyz", se_A)
        write(SLAB_OUT / f"{c}_faceB.xyz", se_B)

        # Surface compositions
        cnt_A = surface_composition(se_A)
        cnt_B = surface_composition(se_B)
        log(f"  face A bottom: Li={cnt_A.get('Li',0)} S={cnt_A.get('S',0)} "
            f"P={cnt_A.get('P',0)} Cl={cnt_A.get('Cl',0)} Br={cnt_A.get('Br',0)}  "
            f"total={cnt_A.get('total',0)}")
        log(f"  face B bottom: Li={cnt_B.get('Li',0)} S={cnt_B.get('S',0)} "
            f"P={cnt_B.get('P',0)} Cl={cnt_B.get('Cl',0)} Br={cnt_B.get('Br',0)}  "
            f"total={cnt_B.get('total',0)}")

        comp_result = {
            'comp':            c,
            'family':          info['family'],
            'gaps':            D_VALUES,
            'registries':      [r[0] for r in ALL_REG],
            'E_ncm_iso':       E_ncm_iso,
            'face_A_surface':  cnt_A,
            'face_B_surface':  cnt_B,
            'faces':           {},
        }

        for face_name, se_var in [('A', se_A), ('B', se_B)]:
            # E_se_iso for this face (vacuum on top)
            se_iso = se_var.copy()
            cell_iso = se_iso.cell.array.copy()
            cell_iso[2, 2] += VACUUM_TOP
            se_iso.set_cell(cell_iso, scale_atoms=False)
            se_iso.set_pbc([True, True, True])
            se_iso.calc = calc
            E_se_var = float(se_iso.get_potential_energy())
            log(f"  face {face_name}: E_se_iso = {E_se_var:.4f} eV")

            face_data = {
                'E_se_iso':    E_se_var,
                'per_reg':     {},
                'Wad_samples': {f"{g:.3f}": [] for g in D_VALUES},
            }

            t_face = time.time()
            for reg_name, shift in ALL_REG:
                reg_curve = {}
                for d in D_VALUES:
                    idx += 1
                    try:
                        stacked = stack_interface(se_var, ncm, d, shift)
                        stacked.calc = calc
                        E_int = float(stacked.get_potential_energy())
                        A = xy_area(stacked.cell.array)
                        Wad = -(E_int - E_se_var - E_ncm_iso) / A * 16.0218
                        reg_curve[f"{d:.3f}"] = {
                            'E_int': E_int, 'Wad_J_per_m2': Wad, 'area_A2': A,
                        }
                        face_data['Wad_samples'][f"{d:.3f}"].append(Wad)
                    except Exception as e:
                        reg_curve[f"{d:.3f}"] = {'E_int': None, 'error': str(e)}
                face_data['per_reg'][reg_name] = {'shift': list(shift), 'curve': reg_curve}
                if idx % 100 == 0:
                    el = time.time() - t_global
                    eta = el * (n_total - idx) / idx
                    log(f"    progress {idx}/{n_total}  ({c} face{face_name} {reg_name})  "
                        f"el={el/60:.1f}min ETA={eta/60:.1f}min")

            # 36-reg mean
            wad_mean, wad_std = [], []
            for d in D_VALUES:
                samples = face_data['Wad_samples'][f"{d:.3f}"]
                wad_mean.append(float(np.mean(samples)) if samples else None)
                wad_std.append(float(np.std(samples))   if samples else None)
            face_data['Wad_mean'] = wad_mean
            face_data['Wad_std']  = wad_std
            valid = np.array([m for m in wad_mean if m is not None])
            face_data['Wad_well_mean'] = float(np.nanmax(valid))
            face_data['Wad_asymp_mean'] = float(wad_mean[-1])
            log(f"  [{c} face {face_name}]  Wad_well = {face_data['Wad_well_mean']:+.4f}  "
                f"asymp = {face_data['Wad_asymp_mean']:+.4f}  ({(time.time()-t_face)/60:.1f} min)")

            comp_result['faces'][face_name] = face_data

        json.dump(comp_result, open(OUT / f"{c}_done.json", 'w'), indent=2)

        # Per-comp summary
        wA = comp_result['faces']['A']['Wad_well_mean']
        wB = comp_result['faces']['B']['Wad_well_mean']
        aA = comp_result['faces']['A']['Wad_asymp_mean']
        aB = comp_result['faces']['B']['Wad_asymp_mean']
        log(f"  ─── {c} summary ───")
        log(f"     face A: well = {wA:+.4f}   asymp = {aA:+.4f}")
        log(f"     face B: well = {wB:+.4f}   asymp = {aB:+.4f}")
        log(f"     ΔWad (B − A) at well = {wB-wA:+.4f}   asymp = {aB-aA:+.4f}")

        summary[c] = {
            'family':      info['family'],
            'Wad_well_A':  wA, 'Wad_asymp_A': aA, 'cnt_A': cnt_A,
            'Wad_well_B':  wB, 'Wad_asymp_B': aB, 'cnt_B': cnt_B,
            'dWad_BminusA_well':  wB - wA,
        }
        gc.collect()

    json.dump(summary, open(OUT / 'summary.json', 'w'), indent=2)

    log("\n" + "=" * 70)
    log("INTERPRETATION:")
    log("  • If face A ≈ face B per comp → slab symmetric → flip changes nothing")
    log("  • If face A << face B → original was binding-weak side; flip is canonical")
    log("  • Pick max(A,B) per comp → 'best' termination representative")
    log("  • Compare R(best, paper) to OLD figure R=+0.93")
    log("=" * 70)
    log(f"TOTAL: {(time.time()-t_global)/60:.1f} min")


if __name__ == "__main__":
    main()
