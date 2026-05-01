"""comp1 v2 champion → DFT EOS input 생성

Mirrored from KISTI: /scratch/x3430a02/kgy/manuscript_support/pipeline_v2/comp1_lpscl/step3_dft_eos.py
NOTE: KISTI 원본은 ntyp=3 하드코딩 bug였음 — sed로 4로 정정 (2026-05-01).
이 local 버전은 fixed (ntyp=4).
"""
import numpy as np
from ase.io import read

atoms = read('comp1_v2_rank1_annealed.xyz')
cell = atoms.get_cell().array
sp = atoms.get_chemical_symbols()
frac = atoms.get_scaled_positions()

print(f"Champion: {len(atoms)} atoms")
print(f"Cell: a={np.linalg.norm(cell[0]):.4f}")

# DFT input 생성: v097~v107
for v_pct in range(97, 108):
    scale = (v_pct / 100.0) ** (1.0/3.0)
    new_cell = cell * scale

    fname = f'comp1_v2_eos_v{v_pct:03d}.in'
    with open(fname, 'w') as f:
        f.write(f"""&CONTROL
  calculation='relax'
  prefix='comp1_v2_v{v_pct:03d}'
  pseudo_dir = '/home01/x3430a02/pseudo/SSSP_1.3.0_PBE_efficiency/'
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
  ntyp=4
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
  Li   6.941  li_pbe_v1.4.uspp.F.UPF
  P    30.974  P.pbe-n-rrkjus_psl.1.0.0.UPF
  S    32.065  s_pbe_v1.4.uspp.F.UPF
  Cl   35.453  cl_pbe_v1.4.uspp.F.UPF

K_POINTS automatic
  2 2 2  0 0 0

ATOMIC_POSITIONS (crystal)
""")
        for i in range(len(sp)):
            f.write(f"  {sp[i]:4s}  {frac[i][0]:.10f}  {frac[i][1]:.10f}  {frac[i][2]:.10f}\n")

    import os
    os.makedirs(f'tmp_v{v_pct:03d}', exist_ok=True)

print(f"\nCreated 11 DFT inputs: comp1_v2_eos_v097~v107.in")
print(f"ntyp=4 (Li,P,S,Cl)")
