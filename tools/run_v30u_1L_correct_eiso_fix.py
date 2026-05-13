"""run_v30u_1L_correct_eiso_fix.py — E_ncm reference cell fix.

================================================================================
 HYPOTHESIS
================================================================================
In run_v30u_1L_correct.py, Wad has a per-comp asymp baseline shift:
  comp1 (Li6, v2 slab)    asymp Wad ≈ -3.06 J/m²
  comp2 (Li6, v2 slab)    asymp Wad ≈ -2.92 J/m²
  comp4 (Li5.4, v1 slab)  asymp Wad ≈ -0.41 J/m²
  modelC                  asymp Wad ≈ -3.35 J/m²
This shift should be ~0 (Wad → 0 at infinite separation). The cause:

  E_ncm_iso uses NCM's OWN cell (ncm.cell.array)        ← stack_interface NOT applied
  E_int uses SE cell with NCM atoms placed inside       ← stack_interface used

When NCM cell != SE cell, NCM atoms-in-SE-cell have artifacts (broken
periodicity, image interactions) that exist in E_int but NOT in E_ncm_iso.
The artifacts don't cancel → constant offset in Wad → asymp shift.

================================================================================
 FIX
================================================================================
Recompute E_ncm_iso with NCM placed in SE cell + 30 Å vacuum (matching the
combined system's NCM environment, sans SE). This restores cell consistency.

The fix is mathematically a per-comp constant offset:
   ΔWad = (E_ncm_iso_new - E_ncm_iso_old) / A × 16.0218 [J/m²]
   Wad_corrected(z, reg, gap) = Wad_raw(z, reg, gap) + ΔWad

Therefore we DO NOT re-run the 2880 SCFs per comp — only 1 SCF per comp for
the new E_ncm reference. E_int and E_se are reused from existing JSON.

  Cost: 4 SCFs total (~5 min)
  Output: v30u_1L_correct_results_eiso_fix/{comp}_done.json
          (same schema as v30u_1L_correct, with Wad values shifted)

================================================================================
 REFERENCES TO ORIGINAL CODE (run_v30u_1L_correct.py)
================================================================================
1. stack_interface() lines 70–87: NCM atom positions (wrap in NCM cell,
   translate so min_z=0) are PRESERVED in our reference build below — we just
   stop before adding SE and apply SE cell + vacuum.
2. add_vacuum() line 62: same VACUUM_TOP=30 Å, scale_atoms=False.
3. xy_area() line 90: same area definition.
4. COMPS dict line 21: identical (comp1, comp2, comp4, modelC).
5. Wad formula line 213: Wad = -(E_int - E_se - E_ncm)/A × 16.0218. We add
   the offset without recomputing E_int.

Run on gabia:
  cd /data/work/v30u_ensemble
  python3 run_v30u_1L_correct_eiso_fix.py
"""
import json, time, gc
from pathlib import Path
import numpy as np
from ase.io import read

# ─── CONFIG (matches run_v30u_1L_correct.py) ────────────────────────────────
COMPS = {
    'comp1':  {'se': 'comp1_slab_v2.xyz',            'ncm': 'ncm_7x7x1_PRESERVED.xyz'},
    'comp2':  {'se': 'comp2_slab_v2.xyz',            'ncm': 'ncm_7x7x1_PRESERVED.xyz'},
    'comp4':  {'se': 'comp4_slab_v1_PRESERVED.xyz',  'ncm': 'ncm_5x5x1_PRESERVED.xyz'},
    'modelC': {'se': 'modelC_slab_v2_PRESERVED.xyz', 'ncm': 'ncm_5x5x1_PRESERVED.xyz'},
}
VACUUM_TOP = 30.0  # matches run_v30u_1L_correct.py line 42

WORK = Path('/data/work/v30u_ensemble')
RESULTS_OLD = WORK / 'v30u_1L_correct_results'
RESULTS_NEW = WORK / 'v30u_1L_correct_results_eiso_fix'
RESULTS_NEW.mkdir(exist_ok=True)


def log(msg):
    s = f"[{time.strftime('%H:%M:%S')}] {msg}"
    print(s, flush=True)


# ─── REFERENCE BUILDERS ─────────────────────────────────────────────────────

def ncm_in_se_cell(se, ncm):
    """Place NCM atoms in SE cell + 30 Å vacuum.

    Mirrors run_v30u_1L_correct.py stack_interface() (line 70) for NCM-side,
    omitting:
      - xy shift (shift_frac=(0,0), R1_origin canonical reference)
      - SE addition
    The result has IDENTICAL NCM atom positions to stack_interface's NCM
    contribution at shift_frac=(0,0), in SE cell with vacuum.
    """
    ncm_a = ncm.copy()
    # Step 1: wrap NCM in its OWN cell (matches stack_interface line 76,
    # which wraps in NCM cell because cell hasn't been swapped yet).
    ncm_a.wrap()
    # Step 2: translate z so min z = 0  (line 77).
    ncm_a.translate([0, 0, -ncm_a.positions[:, 2].min()])
    # Step 3: swap to SE cell xy + z = ncm_thickness + 30 Å vacuum.
    # In stack_interface (line 82-85) the cell becomes SE cell xy with
    # z = z_extent_combined + 30 Å. For iso (no SE), z_extent = ncm thickness.
    z_extent = ncm_a.positions[:, 2].max() - ncm_a.positions[:, 2].min()
    new_cell = se.cell.array.copy()
    new_cell[2] = [0, 0, z_extent + VACUUM_TOP]
    ncm_a.set_cell(new_cell, scale_atoms=False)
    ncm_a.set_pbc([True, True, True])
    return ncm_a


def xy_area(cell):
    """Area of xy face — matches run_v30u_1L_correct.py xy_area() line 90."""
    a1 = cell[0]; a2 = cell[1]
    cross = np.cross(a1[:2].tolist() + [0], a2[:2].tolist() + [0])
    return float(np.linalg.norm(cross))


# ─── UMA CALCULATOR (lazy) ──────────────────────────────────────────────────

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
    log("=" * 70)
    log("E_ncm reference cell FIX — recompute E_ncm_iso in SE cell")
    log("=" * 70)
    log("\nLoading UMA-s-1p1...")
    calc = make_calc()
    log("UMA loaded.\n")

    summary = {}
    for c, paths in COMPS.items():
        old_json = RESULTS_OLD / f"{c}_done.json"
        if not old_json.exists():
            log(f"[{c}] MISSING {old_json.name}, skip")
            continue
        old_data = json.load(open(old_json))

        log(f"\n========= {c} =========")
        log(f"  SE: {paths['se']}  |  NCM: {paths['ncm']}")

        se = read(WORK / paths['se'])
        ncm = read(WORK / paths['ncm'])

        # ─── 1. SCF the new NCM iso reference ────────────────────────────
        ncm_se = ncm_in_se_cell(se, ncm)
        A_se = xy_area(ncm_se.cell.array)
        A_ncm_native = xy_area(ncm.cell.array)
        ncm_se.calc = calc
        E_ncm_new = float(ncm_se.get_potential_energy())

        E_ncm_old = old_data['E_ncm_iso']
        dE  = E_ncm_new - E_ncm_old              # eV
        dWad = dE / A_se * 16.0218               # J/m²

        log(f"  area  SE_cell  = {A_se:.2f} Å²")
        log(f"  area  NCM_cell = {A_ncm_native:.2f} Å²   "
            f"(ratio SE/NCM = {A_se/A_ncm_native:.4f})")
        log(f"  E_ncm_iso  OLD (NCM cell) = {E_ncm_old:.4f} eV")
        log(f"  E_ncm_iso  NEW (SE cell)  = {E_ncm_new:.4f} eV")
        log(f"  ΔE_ncm                    = {dE:+.4f} eV")
        log(f"  ΔWad correction           = {dWad:+.4f} J/m²")

        # ─── 2. Apply per-comp constant Wad shift to all (z, reg, gap) ───
        new_results = {z_key: {} for z_key in old_data['Wad_per_z_per_reg']}
        new_wad_samples = {gk: [] for gk in old_data['Wad_samples']}

        for z_key, regs in old_data['Wad_per_z_per_reg'].items():
            for reg_name, reg in regs.items():
                new_curve = {}
                for d_key, dat in reg['curve'].items():
                    if dat.get('Wad_J_per_m2') is not None:
                        w_new = float(dat['Wad_J_per_m2']) + dWad
                        new_curve[d_key] = {
                            'E_int':       dat.get('E_int'),
                            'Wad_J_per_m2': w_new,
                            'area_A2':     dat.get('area_A2'),
                        }
                        new_wad_samples[d_key].append(w_new)
                    else:
                        new_curve[d_key] = dat
                new_results[z_key][reg_name] = {
                    'shift': reg['shift'], 'curve': new_curve
                }

        # ─── 3. Build corrected JSON ─────────────────────────────────────
        corrected = dict(old_data)  # shallow copy
        corrected['E_ncm_iso']                = E_ncm_new   # primary reference now
        corrected['E_ncm_iso_OLD_NCM_cell']   = E_ncm_old
        corrected['E_ncm_iso_NEW_SE_cell']    = E_ncm_new
        corrected['delta_E_ncm_eV']           = dE
        corrected['delta_Wad_J_per_m2']       = dWad
        corrected['area_SE_cell_A2']          = A_se
        corrected['area_NCM_cell_A2']         = A_ncm_native
        corrected['Wad_per_z_per_reg']        = new_results
        corrected['Wad_samples']              = new_wad_samples
        corrected['Wad_mean']                 = []
        corrected['Wad_std']                  = []
        for g in old_data['gaps']:
            gk = f"{g:.3f}"
            samples = new_wad_samples[gk]
            if samples:
                corrected['Wad_mean'].append(float(np.mean(samples)))
                corrected['Wad_std'].append(float(np.std(samples)))
            else:
                corrected['Wad_mean'].append(None)
                corrected['Wad_std'].append(None)

        json.dump(corrected, open(RESULTS_NEW / f"{c}_done.json", 'w'), indent=2)

        # ─── 4. Summary print (before vs after) ──────────────────────────
        old_mean = np.array(old_data['Wad_mean'], dtype=float)
        new_mean = np.array(corrected['Wad_mean'], dtype=float)
        log(f"  Wad asymp (last gap={old_data['gaps'][-1]:.1f}Å):")
        log(f"       OLD = {old_mean[-1]:+.4f}  NEW = {new_mean[-1]:+.4f}")
        log(f"  Wad well max:")
        log(f"       OLD = {np.nanmax(old_mean):+.4f}  NEW = {np.nanmax(new_mean):+.4f}")
        log(f"  Wad well @ d=1.6 Å:")
        if '1.600' in old_data['Wad_samples']:
            i_16 = old_data['gaps'].index(1.6)
            log(f"       OLD = {old_mean[i_16]:+.4f}  NEW = {new_mean[i_16]:+.4f}")

        summary[c] = {
            'E_ncm_old_eV':  E_ncm_old,
            'E_ncm_new_eV':  E_ncm_new,
            'dE_eV':         dE,
            'dWad_J_per_m2': dWad,
            'area_SE_A2':    A_se,
            'area_NCM_A2':   A_ncm_native,
            'asymp_old':     float(old_mean[-1]),
            'asymp_new':     float(new_mean[-1]),
            'well_max_old':  float(np.nanmax(old_mean)),
            'well_max_new':  float(np.nanmax(new_mean)),
        }
        gc.collect()

    json.dump(summary, open(RESULTS_NEW / 'summary.json', 'w'), indent=2)
    log(f"\nSaved corrected JSONs to: {RESULTS_NEW}")
    log(f"Saved summary: {RESULTS_NEW / 'summary.json'}")
    log("\n" + "=" * 70)
    log("Interpretation:")
    log("  If NEW asymp ≈ 0 across all comps → cell-mismatch hypothesis CONFIRMED")
    log("  If NEW asymp still varies → asymp shift has another origin (run d=10 test)")
    log("=" * 70)


if __name__ == "__main__":
    main()
