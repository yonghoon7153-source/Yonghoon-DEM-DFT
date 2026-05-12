"""anneal_md.py — 500K 100ps Langevin MD with internal 25ps checkpoint.
RESUMABLE: saves state every 25ps; on restart reads state and continues.

Usage: python anneal_md.py <rank> <li_rank>
  rank: halogen rank (0-4)
  li_rank: top-N Li ordering for that rank (0-4)

Output (per (rank, li)):
  rank{R}_li{L}_md.xyz       last saved structure
  rank{R}_li{L}_md.vel.npy   velocities
  rank{R}_li{L}_md.json      progress {steps_done, done}

When 100ps done: writes 'done': true → next call exits 0 immediately.
"""
import sys, json, time, os
from pathlib import Path
import numpy as np
from pymatgen.core import Structure
from pymatgen.io.ase import AseAtomsAdaptor
from ase import units
from ase.md.langevin import Langevin
from ase.md.velocitydistribution import MaxwellBoltzmannDistribution
from ase.io import write, read
from fairchem.core import pretrained_mlip
from fairchem.core.calculate.ase_calculator import FAIRChemCalculator

RANK = int(sys.argv[1])
LI   = int(sys.argv[2])
TARGET_STEPS = 100000          # 100 ps @ 1 fs
CHECKPOINT_STEPS = 25000       # save every 25 ps

XYZ_PATH = Path(f'rank{RANK}_li{LI}_md.xyz')
VEL_PATH = Path(f'rank{RANK}_li{LI}_md.vel.npy')
STATE_PATH = Path(f'rank{RANK}_li{LI}_md.json')

# Done check
if STATE_PATH.exists() and json.load(open(STATE_PATH)).get('done', False):
    print(f"[md rank{RANK} li{LI}] already DONE, exit 0"); sys.exit(0)

# Load Stage 2 cache for this rank
S2_CACHE = Path(f'cache_stage2_rank{RANK}.json')
if not S2_CACHE.exists():
    # Rank 0 fallback
    if RANK == 0 and Path('cache_stage2.json').exists():
        S2_CACHE = Path('cache_stage2.json')
    else:
        print(f"ERROR: {S2_CACHE} not found. Run anneal_stage2.py {RANK} first.")
        sys.exit(2)
cache2 = json.load(open(S2_CACHE))
best_s = cache2['best_s']; best_cl = cache2['best_cl']; best_br = cache2['best_br']
li_results = cache2.get('stage2_li_top20', [])
if LI >= len(li_results):
    print(f"ERROR: LI {LI} out of range (max={len(li_results)-1})"); sys.exit(2)
li_idx = li_results[LI]['li_idx']

# Initialize calc
predictor = pretrained_mlip.get_predict_unit("uma-s-1p1", device="cuda")
adaptor = AseAtomsAdaptor()

# Load or init structure + velocities
if XYZ_PATH.exists() and VEL_PATH.exists() and STATE_PATH.exists():
    a = read(XYZ_PATH)
    a.set_velocities(np.load(VEL_PATH))
    state = json.load(open(STATE_PATH))
    print(f"[md rank{RANK} li{LI}] RESUME from {state['steps_done']}/{TARGET_STEPS}")
else:
    # Build initial
    ref = Structure.from_file('ref_comp3.cif')
    li_sites, p_sites, s_framework, free_sites = [], [], [], []
    for site in ref:
        sp = str(site.specie); fc = site.frac_coords
        if sp == 'Li': li_sites.append(fc)
        elif sp == 'P': p_sites.append(fc)
        else:
            p_coords = np.array(p_sites) if p_sites else np.zeros((1,3))
            dists = ref.lattice.get_all_distances(fc.reshape(1,-1), p_coords)[0]
            if sp == 'S' and len(p_sites) > 0 and min(dists) < 2.5:
                s_framework.append(fc)
            else: free_sites.append(fc)
    species, coords = [], []
    for i in li_idx: species.append('Li'); coords.append(li_sites[i])
    for c in p_sites: species.append('P'); coords.append(c)
    for c in s_framework: species.append('S'); coords.append(c)
    for i, c in enumerate(free_sites):
        if i in best_s: species.append('S')
        elif i in best_cl: species.append('Cl')
        elif i in best_br: species.append('Br')
        else: species.append('Cl')
        coords.append(c)
    s = Structure(ref.lattice, species, coords)
    a = adaptor.get_atoms(s)
    MaxwellBoltzmannDistribution(a, temperature_K=500)
    state = {'rank': RANK, 'li': LI, 'steps_done': 0, 'done': False,
             'started_at': time.strftime('%Y-%m-%d %H:%M:%S')}
    print(f"[md rank{RANK} li{LI}] START fresh (target {TARGET_STEPS} steps)")

a.calc = FAIRChemCalculator(predictor, task_name="omat")

# Save callback (every CHECKPOINT_STEPS)
checkpoint_counter = [0]
def save_checkpoint():
    checkpoint_counter[0] += 1
    write(XYZ_PATH, a)
    np.save(VEL_PATH, a.get_velocities())
    state['steps_done'] += CHECKPOINT_STEPS
    state['last_save'] = time.strftime('%Y-%m-%d %H:%M:%S')
    json.dump(state, open(STATE_PATH, 'w'), indent=2)
    print(f"  checkpoint {checkpoint_counter[0]}: {state['steps_done']}/{TARGET_STEPS} steps", flush=True)

remaining = TARGET_STEPS - state['steps_done']
if remaining <= 0:
    state['done'] = True
    json.dump(state, open(STATE_PATH, 'w'), indent=2)
    print(f"[md rank{RANK} li{LI}] already at target, marked DONE"); sys.exit(0)

t0 = time.time()
print(f"[md rank{RANK} li{LI}] running {remaining} more steps "
      f"(checkpoint every {CHECKPOINT_STEPS})")
dyn = Langevin(a, 1.0*units.fs, temperature_K=500, friction=0.01)
dyn.attach(save_checkpoint, interval=CHECKPOINT_STEPS)
dyn.run(remaining)

# Final save + done flag
write(XYZ_PATH, a)
np.save(VEL_PATH, a.get_velocities())
state['steps_done'] = TARGET_STEPS
state['done'] = True
state['finished_at'] = time.strftime('%Y-%m-%d %H:%M:%S')
state['total_runtime_min'] = (time.time() - t0) / 60
json.dump(state, open(STATE_PATH, 'w'), indent=2)
print(f"[md rank{RANK} li{LI}] DONE 100ps  ({state['total_runtime_min']:.1f} min)")
