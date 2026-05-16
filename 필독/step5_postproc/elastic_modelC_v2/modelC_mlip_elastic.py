import numpy as np
from ase import Atoms, units
from ase.io import read
from ase.md.langevin import Langevin
from ase.md.velocitydistribution import MaxwellBoltzmannDistribution
from ase.optimize import LBFGS
from fairchem.core import pretrained_mlip
from fairchem.core.calculate.ase_calculator import FAIRChemCalculator

predictor = pretrained_mlip.get_predict_unit("uma-s-1p1", device="cuda")

def new_calc():
    return FAIRChemCalculator(predictor, task_name="omat")

def get_cij(atoms, delta=0.005):
    """Relaxed-ion finite strain Cij"""
    cell0 = atoms.get_cell().array.copy()
    pos0 = atoms.get_scaled_positions().copy()
    V = atoms.get_volume()

    patterns = {
        'xx': np.array([[delta,0,0],[0,0,0],[0,0,0]]),
        'yy': np.array([[0,0,0],[0,delta,0],[0,0,0]]),
        'zz': np.array([[0,0,0],[0,0,0],[0,0,delta]]),
        'yz': np.array([[0,0,0],[0,0,delta/2],[0,delta/2,0]]),
        'xz': np.array([[0,0,delta/2],[0,0,0],[delta/2,0,0]]),
        'xy': np.array([[0,delta/2,0],[delta/2,0,0],[0,0,0]]),
    }

    stress_results = {}
    for name, eps in patterns.items():
        stresses = []
        for sign in [+1, -1]:
            strain = np.eye(3) + sign * eps
            a = atoms.copy()
            new_cell = cell0 @ strain
            a.set_cell(new_cell, scale_atoms=True)
            a.calc = new_calc()
            try: LBFGS(a, logfile=None).run(fmax=0.01, steps=50)
            except: pass
            s = a.get_stress(voigt=True)
            stresses.append(s)
        ds = (stresses[0] - stresses[1]) / (2 * delta)
        stress_results[name] = ds * (-160.2)

    C = np.zeros((6,6))
    order = ['xx','yy','zz','yz','xz','xy']
    for j, name in enumerate(order):
        C[:,j] = stress_results[name]
    C = (C + C.T) / 2
    return C

def vrh(C):
    """VRH average from Cij"""
    C11,C12,C44 = C[0,0], C[0,1], C[3,3]
    K_v = (C[0,0]+C[1,1]+C[2,2]+2*(C[0,1]+C[0,2]+C[1,2]))/9
    G_v = ((C[0,0]+C[1,1]+C[2,2])-(C[0,1]+C[0,2]+C[1,2])+3*(C[3,3]+C[4,4]+C[5,5]))/15
    S = np.linalg.inv(C)
    K_r = 1/((S[0,0]+S[1,1]+S[2,2])+2*(S[0,1]+S[0,2]+S[1,2]))
    G_r = 15/(4*(S[0,0]+S[1,1]+S[2,2])-4*(S[0,1]+S[0,2]+S[1,2])+3*(S[3,3]+S[4,4]+S[5,5]))
    K = (K_v+K_r)/2
    G = (G_v+G_r)/2
    E = 9*K*G/(3*K+G)
    nu = (3*K-2*G)/(6*K+2*G)
    return C11, C12, C44, K, G, E, nu

atoms = read('modelc_v2_V0.xyz')

# === 1. 300K Unit Cell ===
print("="*60)
print("1. 300K Unit Cell Elastic")
print("="*60, flush=True)
a300 = atoms.copy()
a300.calc = new_calc()
MaxwellBoltzmannDistribution(a300, temperature_K=300)
Langevin(a300, 1*units.fs, temperature_K=300, friction=0.01).run(5000)
try: LBFGS(a300, logfile=None).run(fmax=0.005, steps=100)
except: pass

C = get_cij(a300)
C11,C12,C44,K,G,E,nu = vrh(C)
print(f"  C11={C11:.1f} C12={C12:.1f} C44={C44:.1f}")
print(f"  K={K:.1f} G={G:.1f} E={E:.1f} nu={nu:.3f}", flush=True)

# === 2. 300K 2x2x1 Supercell ===
print("\n" + "="*60)
print("2. 300K 2x2x1 Supercell Elastic")
print("="*60, flush=True)
sc = atoms.repeat((2,2,1))
sc.calc = new_calc()
MaxwellBoltzmannDistribution(sc, temperature_K=300)
Langevin(sc, 1*units.fs, temperature_K=300, friction=0.01).run(5000)
try: LBFGS(sc, logfile=None).run(fmax=0.005, steps=100)
except: pass

C = get_cij(sc)
C11,C12,C44,K,G,E,nu = vrh(C)
print(f"  C11={C11:.1f} C12={C12:.1f} C44={C44:.1f}")
print(f"  K={K:.1f} G={G:.1f} E={E:.1f} nu={nu:.3f}")
print(f"  atoms: {len(sc)}", flush=True)

# === 3. 600K Snapshot (5 snapshots) ===
print("\n" + "="*60)
print("3. 600K Snapshot Elastic (5 snapshots)")
print("="*60, flush=True)
results = []
a600 = atoms.copy()
a600.calc = new_calc()
MaxwellBoltzmannDistribution(a600, temperature_K=600)
Langevin(a600, 1*units.fs, temperature_K=600, friction=0.01).run(10000)

for snap in range(5):
    print(f"  snapshot {snap+1}/5...", flush=True)
    Langevin(a600, 1*units.fs, temperature_K=600, friction=0.01).run(2000)

    sq = a600.copy()
    sq.calc = new_calc()
    try: LBFGS(sq, logfile=None).run(fmax=0.005, steps=200)
    except: pass

    C = get_cij(sq)
    C11,C12,C44,K,G,E,nu = vrh(C)
    results.append([C11,C12,C44,K,G,E,nu])
    print(f"    C11={C11:.1f} C12={C12:.1f} C44={C44:.1f} E={E:.1f}", flush=True)

arr = np.array(results)
print(f"\n  600K Snapshot Average (5 runs):")
labels = ['C11','C12','C44','K','G','E','nu']
for i, lab in enumerate(labels):
    print(f"    {lab}: {arr[:,i].mean():.1f} +- {arr[:,i].std():.1f}")

print("\nv1 reference (Model C):")
print("  300K_unit:  E=28.9")
print("  300K_super: E=29.7")
print("  600K_snap:  E=32.9 +- 0.9")
print("\nALL DONE")
