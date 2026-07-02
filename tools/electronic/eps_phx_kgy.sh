#!/bin/bash
# eps_phx_kgy.sh — eps_inf (clamped-ion dielectric tensor) via ph.x epsil on kgy.
#
# WHY here: epsilon.x rejects our USPP+PAW pseudos ("USPP are not implemented",
# NC-only). ph.x DFPT epsil DOES support USPP. KISTI's ph.x hung (its qe-cpu
# build), but kgy's clean QE 7.4.1 (system gfortran + OpenMPI) may run it. This
# regenerates the b2o3 champion SCF (fixed occ, SSSP auto-pseudo) with ASE, then
# runs ph.x epsil=.true.,trans=.false. -> eps_inf. All CPU (kgy qe-7.4.1-cpu).
#
#   conda activate uma        # (ASE needed for the input step)
#   bash tools/electronic/eps_phx_kgy.sh
# Run inside tmux — the SCF + DFPT take a while (no walltime limit on kgy).
#
# If ph.x here ALSO enumerates 384 phonon reps and stalls (a QE-7.4.1 behavior,
# not build), fall back to NC(ONCV) pseudos + epsilon.x. But try this first: it
# reuses the exact USPP champion and is a one-shot.

set -u
REPO="$HOME/work/Yonghoon-DEM-DFT"
CIF="$REPO/db/structures/b2o3_relaxV0.cif"
PSEUDO="${PSEUDO_DIR:-$HOME/work/pseudo}"
PW="$HOME/apps/qe-7.4.1-cpu/bin/pw.x"
PH="$HOME/apps/qe-7.4.1-cpu/bin/ph.x"
WORK="$HOME/work/b2o3_eps"; mkdir -p "$WORK"; cd "$WORK"
ln -sf "$PSEUDO" pseudo
test -f "$CIF" || { echo "cif 없음: $CIF (git pull 했나?)"; exit 1; }

# 1) SCF input from the champion cif (ASE): fixed occ + SSSP auto-pseudo + 2x2x2 k
echo ">> gen scf_eps.in $(date +%H:%M)"
python3 - "$CIF" "$PSEUDO" <<'PY'
import sys, os, glob
from ase.io import read, write
at = read(sys.argv[1]); pdir = os.path.expanduser(sys.argv[2])
pp = {}
for s in sorted(set(at.get_chemical_symbols())):
    c = glob.glob(f'{pdir}/{s}.*') + glob.glob(f'{pdir}/{s.lower()}[._]*') + glob.glob(f'{pdir}/{s.lower()}_*')
    assert c, f'no pseudo for {s} in {pdir}'
    pp[s] = os.path.basename(sorted(c)[0])
print('  pseudos:', pp)
inp = dict(
    control=dict(calculation='scf', prefix='b2o3', outdir='./tmp', pseudo_dir='./pseudo', verbosity='high'),
    system=dict(ecutwfc=60, ecutrho=480, occupations='fixed'),
    electrons=dict(conv_thr=1e-10, mixing_beta=0.3),
)
write('scf_eps.in', at, format='espresso-in', input_data=inp, pseudopotentials=pp, kpts=(2, 2, 2))
print('  -> scf_eps.in')
PY
[ -f scf_eps.in ] || { echo "입력 생성 실패 (conda activate uma 했나?)"; exit 1; }

# 2) SCF (CPU, 8 ranks). b2o3 is an insulator -> fixed occ must give a gap.
echo ">> SCF $(date +%H:%M)"
mpirun -np 8 "$PW" -in scf_eps.in > scf_eps.out 2>&1
grep -q "JOB DONE" scf_eps.out || { echo "SCF 실패:"; tail -25 scf_eps.out; exit 1; }
grep -iE "highest occupied|lowest unoccupied|number of electrons" scf_eps.out | tail -2

# 3) ph.x epsil (q=0, dielectric only; SERIAL to avoid MPI quirks first)
cat > eps.in <<'EOF'
b2o3 eps_inf (epsil only, no phonons)
&inputph
  prefix = 'b2o3',
  outdir = './tmp',
  epsil = .true.,
  trans = .false.,
  recover = .false.,
  tr2_ph = 1.0d-14,
  fildyn = 'b2o3.dyn',
/
0.0 0.0 0.0
EOF
echo ">> ph.x epsil $(date +%H:%M)  (Representation 384개 나열되며 멈추면 = QE-version 이슈 -> NC+epsilon.x로)"
"$PH" -in eps.in > eps.out 2>&1
echo ">> done $(date +%H:%M)"
echo "==== eps_inf (Dielectric constant in cartesian axis) ===="
grep -A4 "Dielectric constant in cartesian axis" eps.out \
  || { echo "epsil 텐서 없음 — tail:"; tail -30 eps.out; }
