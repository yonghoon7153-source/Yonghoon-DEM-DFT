#!/bin/bash
# eps_epsilon_kisti.sh — electronic dielectric constant (eps_inf) via QE epsilon.x,
# BYPASSING the hanging ph.x. Route: fixed-occupation SCF (already have) -> nscf on
# a dense full k-grid (GPU pw.x, works) -> epsilon.x (independent-particle dielectric
# function eps(w)) -> eps_inf = eps1(w->0). No ph.x, no DFPT, no hang.
#
# Level: IPA/RPA-without-local-fields (interband sum-over-states). This is the
# electronic (clamped-ion) eps_inf estimate; differs from DFPT epsil by local-field
# effects (usually a modest correction), and is the standard cheap route.
#
#   sbatch tools/electronic/eps_epsilon_kisti.sh <fixed_scf.in>
# e.g. sbatch tools/electronic/eps_epsilon_kisti.sh b2o3_scf_fixed.in
# arg = the fixed-occupation SCF input whose tmp_fixed/b2o3.save already exists.
#
#SBATCH -J llm_finetuning_eps
#SBATCH -p amd_a100nv_8
#SBATCH -N 1
#SBATCH --ntasks-per-node=8
#SBATCH --cpus-per-task=1
#SBATCH --gres=gpu:1
#SBATCH --time=04:00:00
#SBATCH --comment pytorch
#SBATCH -o logs/eps_%j.out
#SBATCH -e logs/eps_%j.err
set +H
source /scratch/x3430a02/mjs0000/miniforge3/etc/profile.d/conda.sh 2>/dev/null || true
conda activate uma 2>/dev/null || true
cd "${SLURM_SUBMIT_DIR:-$PWD}"; mkdir -p logs
echo ">> start $(date +%H:%M:%S)  cwd=$(pwd)"

PWX=/scratch/x3430a02/kgy/apps/qe-gpu/bin/pw.x          # GPU nscf (works, no hang)
EPX=/scratch/x3430a02/kgy/apps/qe-cpu/bin/epsilon.x     # epsilon.x (lightweight)
SCF_SRC="${1:-b2o3_scf_fixed.in}"
KGRID="${2:-3 3 3}"      # dense k-grid for the optical sum (can pass "4 4 4")
NBND="${3:-360}"         # occupied ~240 + empty; more empty = spectrum to higher w
test -f "$SCF_SRC" || { echo "ERROR: '$SCF_SRC' 없음. fixed SCF 입력을 arg로."; exit 1; }

# 1) build nscf input for epsilon.x: nscf + fixed occ + nosym/noinv (full k-grid) + nbnd + dense k
python3 - "$SCF_SRC" "$KGRID" "$NBND" <<'PY'
import sys, re
src, kg, nb = open(sys.argv[1]).read(), sys.argv[2], sys.argv[3]
src = re.sub(r"calculation\s*=\s*'[^']*'", "calculation = 'nscf'", src)
src = re.sub(r"prefix\s*=\s*'[^']*'", "prefix = 'b2o3'", src)
src = re.sub(r"outdir\s*=\s*'[^']*'", "outdir = './tmp_fixed'", src)
def set_or_add(key, val, s, nml='&system'):
    if re.search(rf"{key}\s*=", s):
        return re.sub(rf"{key}\s*=\s*[^\n,]+", f"{key} = {val}", s)
    return re.sub(rf"({nml}[^\n]*\n)", rf"\1  {key} = {val},\n", s, count=1, flags=re.I)
# insulator + full BZ (epsilon.x sums the unreduced grid)
if re.search(r"occupations\s*=", src): src = re.sub(r"occupations\s*=\s*'[^']*'", "occupations = 'fixed'", src)
else: src = re.sub(r"(&system[^\n]*\n)", r"\1  occupations = 'fixed'\n", src, count=1, flags=re.I)
src = re.sub(r"[ \t]*smearing\s*=\s*'[^']*'\s*,?\n", "", src)
src = re.sub(r"[ \t]*degauss\s*=\s*[0-9.eEdD+\-]+\s*,?\n", "", src)
src = set_or_add("nbnd", nb, src)
src = set_or_add("nosym", ".true.", src)
src = set_or_add("noinv", ".true.", src)
# dense k-grid: replace whatever K_POINTS block is there
if re.search(r"K_POINTS\s+automatic", src, re.I):
    src = re.sub(r"K_POINTS\s+automatic[^\n]*\n[^\n]*\n", f"K_POINTS automatic\n{kg} 0 0 0\n", src, flags=re.I)
elif re.search(r"K_POINTS\s+gamma", src, re.I):
    src = re.sub(r"K_POINTS\s+gamma[^\n]*\n", f"K_POINTS automatic\n{kg} 0 0 0\n", src, flags=re.I)
else:
    src = src.rstrip() + f"\nK_POINTS automatic\n{kg} 0 0 0\n"
open("nscf_eps.in", "w").write(src)
print(f"-> nscf_eps.in (nscf, fixed occ, nbnd={nb}, K {kg}, nosym/noinv)")
PY

# 2) nscf on GPU
echo ">> nscf $(date +%H:%M:%S)"
mpirun -np 1 "$PWX" -npool 1 -inp nscf_eps.in > nscf_eps.out 2>&1
grep -q "JOB DONE" nscf_eps.out || { echo "NSCF FAILED:"; tail -25 nscf_eps.out; exit 1; }
grep -iE "highest occupied|lowest unoccupied" nscf_eps.out | tail -1

# 3) epsilon.x input
cat > epsilon.in <<'EOF'
&inputpp
  prefix = 'b2o3',
  outdir = './tmp_fixed',
  calculation = 'eps',
/
&energy_grid
  smeartype = 'gauss',
  intersmear = 0.1,
  intrasmear = 0.0,
  wmin = 0.0,
  wmax = 15.0,
  nw = 600,
  shift = 0.0,
/
EOF

# 4) epsilon.x
echo ">> epsilon.x $(date +%H:%M:%S)"
mpirun -np 8 "$EPX" -inp epsilon.in > epsilon.out 2>&1

# 5) eps_inf = eps1(w->0) : first data row of epsr.dat
echo "==== eps_inf (electronic, IPA)  =  eps1(w -> 0) ===="
F=$(ls epsr.dat epsr_b2o3.dat 2>/dev/null | head -1)
if [ -n "$F" ]; then
  python3 -c "
import numpy as np
d=np.loadtxt('$F')
r=d[0]
if len(r)>=4:
    print(f'  w={r[0]:.3f} eV : eps_inf  xx={r[1]:.3f}  yy={r[2]:.3f}  zz={r[3]:.3f}  | avg {np.mean(r[1:4]):.3f}')
else:
    print('  first row:', r)
print('  (full spectrum: $F ; eps2 in epsi.dat)')
"
else
  echo "  epsr.dat 없음 — epsilon.out tail:"; tail -20 epsilon.out; ls -la *.dat 2>/dev/null
fi
echo ">> done $(date +%H:%M:%S)"
