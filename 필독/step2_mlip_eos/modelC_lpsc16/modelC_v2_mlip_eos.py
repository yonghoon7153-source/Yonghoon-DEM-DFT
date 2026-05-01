"""
Model C v2 — Step 4: MLIP EOS
Champion: modelC_v2_champion.xyz (step1 unified output)
Volume scaling 94-108%, BM3 fitting → preliminary V0, B0
"""
import numpy as np
from ase.io import read, write
from ase.optimize import LBFGS
from scipy.optimize import curve_fit
from fairchem.core import pretrained_mlip
from fairchem.core.calculate.ase_calculator import FAIRChemCalculator

predictor = pretrained_mlip.get_predict_unit("uma-s-1p1", device="cuda")

def new_calc():
    return FAIRChemCalculator(predictor, task_name="omat")

def bm3(V, E0, V0, B0, Bp):
    eta = (V0/V)**(2./3.)
    return E0 + 9.*V0*B0/(16.) * ((eta-1)**2 * (6. + Bp*(eta-1) - 4.*eta))

# Load champion
champ = read('modelC_v2_champion.xyz')
cell0 = champ.get_cell().copy()
V_ref = champ.get_volume()
print(f"Champion: {len(champ)} atoms, V_ref={V_ref:.2f} A3")
print(f"Cell: a={np.linalg.norm(cell0[0]):.4f}, b={np.linalg.norm(cell0[1]):.4f}, c={np.linalg.norm(cell0[2]):.4f}")

# Volume scan: 94% to 108%
scales = np.arange(0.94, 1.09, 0.01)
results = []

print(f"\n{'vol%':>6} {'V(A3)':>10} {'E(eV)':>12} {'P(GPa)':>8}")
print("-"*40)

for s in scales:
    atoms = champ.copy()
    # Scale cell uniformly
    new_cell = cell0 * s**(1./3.)
    atoms.set_cell(new_cell, scale_atoms=True)
    atoms.calc = new_calc()

    try:
        LBFGS(atoms, logfile=None).run(fmax=0.01, steps=200)
    except:
        pass

    e = atoms.get_potential_energy()
    v = atoms.get_volume()

    # Pressure from stress
    try:
        stress = atoms.get_stress()
        p = -stress[:3].mean() * 160.2176634  # eV/A3 → GPa
    except:
        p = 0.0

    results.append((v, e, s*100))
    print(f"{s*100:>6.1f} {v:>10.2f} {e:>12.4f} {p:>8.2f}", flush=True)

V_arr = np.array([r[0] for r in results])
E_arr = np.array([r[1] for r in results])

# BM3 fit
try:
    p0 = [E_arr.min(), V_arr[E_arr.argmin()], 0.02/160.2, 4.0]  # E0, V0, B0(eV/A3), Bp
    popt, pcov = curve_fit(bm3, V_arr, E_arr, p0=p0, maxfev=10000)
    E0, V0, B0_evA3, Bp = popt
    B0_GPa = B0_evA3 * 160.2176634

    E_fit = bm3(V_arr, *popt)
    SS_res = np.sum((E_arr - E_fit)**2)
    SS_tot = np.sum((E_arr - E_arr.mean())**2)
    R2 = 1 - SS_res/SS_tot

    print(f"\n{'='*50}")
    print(f"BM3 FIT RESULTS")
    print(f"  V0 = {V0:.2f} A3")
    print(f"  B0 = {B0_GPa:.1f} GPa")
    print(f"  B0'= {Bp:.2f}")
    print(f"  E0 = {E0:.4f} eV")
    print(f"  R2 = {R2:.6f}")
    print(f"  v1 B0 = 21.7 GPa (Basin A)")
    print(f"  Delta = {B0_GPa - 21.7:+.1f} GPa")
    print(f"{'='*50}")

    # V0 as percentage of V_ref
    v0_pct = V0/V_ref * 100
    print(f"  V0 = v{v0_pct:.1f} (for DFT grid)")
    print(f"  DFT range suggestion: v{v0_pct-5:.0f} - v{v0_pct+5:.0f}")
except Exception as e:
    print(f"\nBM3 fit FAILED: {e}")
    print("Check data for basin transitions!")

print("\nDone! Next: DFT EOS at suggested volume range.")
