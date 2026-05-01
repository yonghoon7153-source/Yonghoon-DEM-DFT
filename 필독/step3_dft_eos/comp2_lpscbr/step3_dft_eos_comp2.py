"""comp2 v2 champion → DFT EOS input 생성 (v098-v108, 11 volumes)

Mirrored from KISTI: /scratch/x3430a02/kgy/manuscript_support/pipeline_v2/comp2_lpscbr/step3_dft_eos_comp2.py
"""
import numpy as np
import os
from ase.io import read

atoms = read('comp2_v2_champion.xyz')
cell = atoms.get_cell().array
sp = atoms.get_chemical_symbols()
frac = atoms.get_scaled_positions()

# Verify composition
counts = {s: sp.count(s) for s in sorted(set(sp))}
print(f"Champion: {len(atoms)} atoms, {counts}")
print(f"Cell: a={np.linalg.norm(cell[0]):.4f} A")

# DFT input 생성: v098~v108 (11 vol, MLIP EOS 추천 range)
N_TYP = len(set(sp))
print(f"ntyp = {N_TYP} (species: {sorted(set(sp))})")

for v_pct in range(98, 109):
    scale = (v_pct / 100.0) ** (1.0/3.0)
    new_cell = cell * scale

    fname = f'comp2_v2_eos_v{v_pct:03d}.in'
    with open(fname, 'w') as f:
        f.write(f"""&CONTROL
  calculation='relax'
  prefix='comp2_v2_v{v_pct:03d}'
  pseudo_dir = '/scratch/x3430a02/kgy/manuscript_support/pseudo/'
  outdir = './tmp_v{v_pct:03d}/'
  tprnfor=.true.
  tstress=.true.
  etot_conv_thr=1.0d-6
  forc_conv_thr=1.0d-4
  nstep=200
/
&SYSTEM
  ibrav=0
  nat={len(atoms)}
  ntyp={N_TYP}
  ecutwfc=52
  ecutrho=520
  occupations='smearing'
  smearing='mv'
  degauss=0.01
  nosym=.true.
/
&ELECTRONS
  conv_thr=1.0d-8
  mixing_beta=0.2
  electron_maxstep=200
/
&IONS
  ion_dynamics='bfgs'
/

CELL_PARAMETERS angstrom
""")
        for row in new_cell:
            f.write(f"  {row[0]:.10f}  {row[1]:.10f}  {row[2]:.10f}\n")

        f.write("""
ATOMIC_SPECIES
  Li   6.941   li_pbe_v1.4.uspp.F.UPF
  P    30.974  P.pbe-n-rrkjus_psl.1.0.0.UPF
  S    32.065  s_pbe_v1.4.uspp.F.UPF
  Cl   35.453  cl_pbe_v1.4.uspp.F.UPF
  Br   79.904  br_pbe_v1.4.uspp.F.UPF

K_POINTS automatic
  2 2 2  0 0 0

ATOMIC_POSITIONS (crystal)
""")
        for i in range(len(sp)):
            f.write(f"  {sp[i]:4s}  {frac[i][0]:.10f}  {frac[i][1]:.10f}  {frac[i][2]:.10f}\n")

    os.makedirs(f'tmp_v{v_pct:03d}', exist_ok=True)

print(f"\nCreated 11 DFT inputs: comp2_v2_eos_v098 ~ v108.in")
print(f"Ready for KISTI GPU execution")
