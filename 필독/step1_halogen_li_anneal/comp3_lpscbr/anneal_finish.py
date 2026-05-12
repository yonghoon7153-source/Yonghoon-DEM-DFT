"""anneal_finish.py — 300K quench (10ps) + LBFGS relax for one (rank, li).
Reads MD final state from anneal_md.py output.

Usage: python anneal_finish.py <rank> <li>
Output: rank{R}_li{L}_anneal.xyz   final relaxed structure
        rank{R}_li{L}_anneal.json  {E_init, E_after, e_before_md, ...}
Time: ~15 min (10ps quench + LBFGS). Fits any walltime.
"""
import sys, json, time
from pathlib import Path
import numpy as np
from ase import units
from ase.md.langevin import Langevin
from ase.optimize import LBFGS
from ase.io import write, read
from fairchem.core import pretrained_mlip
from fairchem.core.calculate.ase_calculator import FAIRChemCalculator

RANK = int(sys.argv[1])
LI   = int(sys.argv[2])

OUT_XYZ = Path(f'rank{RANK}_li{LI}_anneal.xyz')
OUT_JSON = Path(f'rank{RANK}_li{LI}_anneal.json')

if OUT_JSON.exists():
    print(f"[finish rank{RANK} li{LI}] already DONE"); sys.exit(0)

# Need MD done
MD_STATE = Path(f'rank{RANK}_li{LI}_md.json')
MD_XYZ = Path(f'rank{RANK}_li{LI}_md.xyz')
MD_VEL = Path(f'rank{RANK}_li{LI}_md.vel.npy')
if not all(p.exists() for p in [MD_STATE, MD_XYZ, MD_VEL]):
    print(f"ERROR: MD outputs missing. Run anneal_md.py {RANK} {LI} first."); sys.exit(2)
md_state = json.load(open(MD_STATE))
if not md_state.get('done', False):
    print(f"ERROR: MD not complete ({md_state.get('steps_done',0)}/100000)"); sys.exit(2)

t0 = time.time()
a = read(MD_XYZ)
a.set_velocities(np.load(MD_VEL))
predictor = pretrained_mlip.get_predict_unit("uma-s-1p1", device="cuda")
a.calc = FAIRChemCalculator(predictor, task_name="omat")
E_pre_quench = float(a.get_potential_energy())

print(f"[finish rank{RANK} li{LI}] 300K 10ps quench...")
Langevin(a, 1.0*units.fs, temperature_K=300, friction=0.05).run(10000)
E_post_quench = float(a.get_potential_energy())
print(f"  E after quench = {E_post_quench:.4f}")

print(f"[finish rank{RANK} li{LI}] LBFGS relax...")
try: LBFGS(a, logfile=None).run(fmax=0.005, steps=300)
except: pass
E_after = float(a.get_potential_energy())
print(f"  E after LBFGS = {E_after:.4f}")

write(OUT_XYZ, a)
json.dump({
    'rank': RANK, 'li': LI,
    'E_pre_quench': E_pre_quench,
    'E_post_quench': E_post_quench,
    'E_after': E_after,
    'runtime_min': (time.time()-t0)/60,
    'finished_at': time.strftime('%Y-%m-%d %H:%M:%S'),
}, open(OUT_JSON, 'w'), indent=2)
print(f"[finish rank{RANK} li{LI}] DONE  E_after={E_after:.4f}  ({(time.time()-t0)/60:.1f} min)")
