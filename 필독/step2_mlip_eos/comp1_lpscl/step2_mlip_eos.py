import numpy as np
from ase.io import read
from ase.optimize import LBFGS
from scipy.optimize import curve_fit
from fairchem.core import pretrained_mlip
from fairchem.core.calculate.ase_calculator import FAIRChemCalculator

predictor = pretrained_mlip.get_predict_unit("uma-s-1p1", device="cuda")
calc = FAIRChemCalculator(predictor, task_name="omat")

atoms = read('comp1_v2_rank1_annealed.xyz')
atoms.calc = calc
try:
    LBFGS(atoms, logfile=None).run(fmax=0.005, steps=300)
except: pass

E0_relax = atoms.get_potential_energy()
cell0 = atoms.get_cell().copy()
V0_cell = abs(np.linalg.det(cell0))
print(f"Champion: {len(atoms)} atoms, E={E0_relax:.4f} eV")
print(f"Cell V = {V0_cell:.2f} A^3")

# EOS: v096~v108
def BM(V,E0,V0,B0,B0p):
    eta=(V0/V)**(2/3)
    return E0+9*V0*B0/16*((eta-1)**3*B0p+(eta-1)**2*(6-4*eta))

volumes = []
energies = []
print(f"\n=== MLIP EOS ===")
for v_pct in range(96, 109):
    scale = (v_pct / 100.0) ** (1.0/3.0)
    a = atoms.copy()
    a.set_cell(cell0 * scale, scale_atoms=True)
    a.calc = calc
    try:
        LBFGS(a, logfile=None).run(fmax=0.01, steps=100)
    except: pass
    e = a.get_potential_energy()
    V = abs(np.linalg.det(a.get_cell()))
    volumes.append(V)
    energies.append(e)
    print(f"  v{v_pct:03d}: V={V:.1f}, E={e:.4f} eV", flush=True)

V_arr = np.array(volumes)
E_arr = np.array(energies)
popt, _ = curve_fit(BM, V_arr, E_arr,
                    [min(E_arr), V_arr[np.argmin(E_arr)], 20/160.2, 4],
                    maxfev=10000)
E0, V0, B0, B0p = popt
B0_GPa = B0 * 160.2
R2 = 1 - np.sum((E_arr - BM(V_arr, *popt))**2) / np.sum((E_arr - np.mean(E_arr))**2)

print(f"\n=== MLIP EOS Results ===")
print(f"  B0 = {B0_GPa:.1f} GPa")
print(f"  B0' = {B0p:.2f}")
print(f"  V0 = {V0:.2f} A^3")
print(f"  R2 = {R2:.6f}")

# DFT용 volume grid 제안
V0_scale = V0 / V0_cell
grid = int(round(V0_scale * 100))
print(f"\n=== DFT 권장 volume grid ===")
print(f"  V0/V_cell = {V0_scale:.4f}")
print(f"  V0 nearest grid: v{grid:03d}")
print(f"  DFT range: v{grid-5:03d} ~ v{grid+5:03d}")

# 비교
print(f"\n=== v1 vs v2 비교 ===")
print(f"  v1 (Rietveld Li): B0=26.2 GPa")
print(f"  v2 (annealing):   B0={B0_GPa:.1f} GPa")
