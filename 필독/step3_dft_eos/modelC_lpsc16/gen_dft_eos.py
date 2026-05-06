"""Model C v2 champion → DFT EOS input 생성 (v096-v106, 11 volumes)
Unified template with comp1/comp2 (ATOMIC_POSITIONS crystal, nosym, nstep).
Numerical settings (ecutwfc=60, K=6x6x3) tuned for rhombohedral cell.
"""
import numpy as np
import os
from ase.io import read

champ = read('modelC_v2_champion.xyz')
cell = champ.get_cell().array
sp = champ.get_chemical_symbols()
frac = champ.get_scaled_positions()

# Verify composition
counts = {s: sp.count(s) for s in sorted(set(sp))}
print(f"Champion: {len(champ)} atoms, {counts}")
print(f"Cell: a={np.linalg.norm(cell[0]):.4f} A")

PP = {
    'Li': 'li_pbe_v1.4.uspp.F.UPF',
    'P':  'P.pbe-n-rrkjus_psl.1.0.0.UPF',
    'S':  's_pbe_v1.4.uspp.F.UPF',
    'Cl': 'cl_pbe_v1.4.uspp.F.UPF',
}
MASS = {'Li': 6.941, 'P': 30.974, 'S': 32.065, 'Cl': 35.453}
PSEUDO_DIR = '/scratch/x3430a02/kgy/manuscript_support/pseudo'

species_order = []
for s in sp:
    if s not in species_order:
        species_order.append(s)
N_TYP = len(species_order)
print(f"ntyp = {N_TYP} (species: {species_order})")

# DFT input 생성: v096~v106 (11 vol, MLIP EOS 추천 range)
for v_pct in range(96, 107):
    scale = (v_pct / 100.0) ** (1.0/3.0)
    new_cell = cell * scale

    fname = f'modelC_v2_eos_v{v_pct:03d}.in'
    with open(fname, 'w') as f:
        f.write(f"""&CONTROL
  calculation='relax'
  prefix='modelC_v2_v{v_pct:03d}'
  pseudo_dir = '{PSEUDO_DIR}'
  outdir = './tmp_v{v_pct:03d}/'
  tprnfor=.true.
  tstress=.true.
  etot_conv_thr=1.0d-6
  forc_conv_thr=1.0d-4
  nstep=200
/
&SYSTEM
  ibrav=0
  nat={len(sp)}
  ntyp={N_TYP}
  ecutwfc=60.0
  ecutrho=480.0
  occupations='smearing'
  smearing='mv'
  degauss=0.01
  nosym=.true.
/
&ELECTRONS
  conv_thr=1.0d-8
  mixing_beta=0.3
  electron_maxstep=200
/
&IONS
  ion_dynamics='bfgs'
/

CELL_PARAMETERS angstrom
""")
        for row in new_cell:
            f.write(f"  {row[0]:.10f}  {row[1]:.10f}  {row[2]:.10f}\n")

        f.write("\nATOMIC_SPECIES\n")
        for s in species_order:
            f.write(f"  {s:4s} {MASS[s]:10.4f}  {PP[s]}\n")

        f.write(f"""
K_POINTS automatic
  6 6 3  0 0 0

ATOMIC_POSITIONS (crystal)
""")
        for i in range(len(sp)):
            f.write(f"  {sp[i]:4s}  {frac[i][0]:.10f}  {frac[i][1]:.10f}  {frac[i][2]:.10f}\n")

    os.makedirs(f'tmp_v{v_pct:03d}', exist_ok=True)

print(f"\nCreated 11 DFT inputs: modelC_v2_eos_v096 ~ v106.in")
print(f"Ready for KISTI GPU execution")
